# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

import os
from typing import Annotated, TypedDict, List, Dict, Any
from dotenv import load_dotenv
from git import Repo
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import Language
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_chroma import Chroma
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AnyMessage
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState
from prompt import spatial_processing_prompt

load_dotenv()

# Configuration
REPO_PATH = "./packages_available/squidpy"
PERSIST_DIRECTORY = "./db/chroma_squidpy_db"

# Define state for Squidpy RAG application
class SquidpyRAGState(TypedDict):
    query: str
    context: List[Document]
    answer: str
    chat_history: List[AnyMessage]

class SquidpyRAGTool:
    def __init__(self, model: str = "claude-3-7-sonnet-20250219"):
        self.model = model
        self.vector_store = self.setup_squidpy_index()
        self.rag_pipeline = self.create_squidpy_rag_pipeline()
    
    def setup_squidpy_index(self):
        """Setup and index the Squidpy repository for RAG if not already done."""
        
        # Clone repo if it doesn't exist
        if not os.path.exists(REPO_PATH):
            print(f"Cloning Squidpy repository to {REPO_PATH}...")
            Repo.clone_from("https://github.com/scverse/squidpy", to_path=REPO_PATH)
        
        # Initialize embeddings
        embeddings = OpenAIEmbeddings(disallowed_special=())
        
        # Load or create vector database
        if not os.path.exists(PERSIST_DIRECTORY):
            print("Creating new Squidpy vector database...")
            
            # Load Python files from the repository
            loader = GenericLoader.from_filesystem(
                REPO_PATH,
                glob="**/*",
                suffixes=[".py"],
                exclude=["**/non-utf8-encoding.py"],
                parser=LanguageParser(language=Language.PYTHON, parser_threshold=500),
            )
            documents = loader.load()
            print(f"Loaded {len(documents)} documents from Squidpy")
            
            # Split documents into chunks
            splitter = RecursiveCharacterTextSplitter.from_language(
                language=Language.PYTHON, chunk_size=2000, chunk_overlap=200
            )
            texts = splitter.split_documents(documents)
            print(f"Split into {len(texts)} text chunks for Squidpy")
            
            # Create vector store
            vector_store = Chroma.from_documents(
                documents=texts,
                embedding=embeddings,
                persist_directory=PERSIST_DIRECTORY
            )
            print(f"Created new Chroma database at {PERSIST_DIRECTORY}")
        else:
            # Load existing vector store
            vector_store = Chroma(
                persist_directory=PERSIST_DIRECTORY,
                embedding_function=embeddings
            )
            print(f"Loaded existing Chroma database from {PERSIST_DIRECTORY}")
        
        return vector_store
    
    def create_squidpy_rag_pipeline(self):
        """Create the RAG pipeline for Squidpy using LangGraph."""
        
        # Initialize the LLM
        llm = ChatAnthropic(model=self.model)
        #llm = ChatOpenAI(model="gpt-4o")
        # Define the retrieval step
        def retrieve(state: SquidpyRAGState):
            """Retrieve relevant documents based on the query."""
            squidpy_retriever = self.vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 8})
            retrieved_docs = squidpy_retriever.invoke(
                state["query"]
            )
            return {"context": retrieved_docs}
        
        # Define the generation step
        def generate(state: SquidpyRAGState):
            """Generate an answer using the retrieved context."""
            # Combine all document content
            context_content = "\n\n".join(doc.page_content for doc in state["context"])
            chat_history = state["chat_history"]
            
            # Create the prompt
            prompt = ChatPromptTemplate.from_messages([
                MessagesPlaceholder("chat_history"),
                ("user", "The above are the CHAT HISTORY between the user and the spatial transcriptomics assistant. you should take into account the chat history when generating the response."),
                ("user", 
                 "You are an expert in Squidpy, specializing in providing authentic Squidpy code "
                 "and explanations on its usage. IMPORTANT: do not use python bracket for the code. "
                 "REPEAT: do not use python bracket for the code. "
                 "For each query, respond with:\n"
                 "1. Squidpy code to solve the user's question.\n"
                 "2. A concise explanation of the code, focusing on Squidpy-specific concepts, "
                 "methods, and relevant parameters.\n\n"
                 "3. REMEMBER to specify shape = None for STARmap spatial transcriptomic data.\n"
                 "The following are some additional instructions:\n"
                 "{spatial_processing_prompt}\n\n"
                 "CONTEXT ON SQUIDPY:\n{context_content}\n\n"
                ),
                ("user", "USER QUESTION: {query}"),
            ])
            
            # Generate messages from the prompt
            messages = prompt.invoke({
                "query": state["query"], 
                "chat_history": chat_history, 
                "context_content": context_content,
                "spatial_processing_prompt": spatial_processing_prompt
            })
            
            # Get response from LLM
            response = llm.invoke(messages)
            
            return {"answer": response.content}
        
        # Build the graph
        graph_builder = StateGraph(SquidpyRAGState)
        graph_builder.add_node("retrieve", retrieve)
        graph_builder.add_node("generate", generate)
        
        # Define the flow
        graph_builder.add_edge(START, "retrieve")
        graph_builder.add_edge("retrieve", "generate")
        graph_builder.add_edge("generate", END)
        
        # Compile the graph
        return graph_builder.compile()
    
    def run(self, query: str, chat_history: List[AnyMessage] = None):
        """Run the Squidpy RAG pipeline with the given query and chat history."""
        if chat_history is None:
            chat_history = []
        
        response = self.rag_pipeline.invoke({
            "query": query,
            "chat_history": chat_history,
            "context": [],  # Will be populated by the retrieve step
            "answer": ""    # Will be populated by the generate step
        })
        
        return response["answer"]

# Initialize the Squidpy RAG tool
squidpy_rag = SquidpyRAGTool()

@tool
def squidpy_rag_agent(state: Annotated[Dict, InjectedState], query: str) -> str:
    """Tool that provides Squidpy code and explanations based on RAG.
    Uses the Squidpy codebase to generate accurate Squidpy code for spatial transcriptomics analysis.
    
    Args:
        query: The query to answer using Squidpy knowledge
        
    Returns:
        str: Code and explanation for the Squidpy query
    """
    # Extract the chat history from the injected state
    #chat_history = state["messages"][:-1]
    chat_history = []
    # Run the Squidpy RAG with the query and chat history
    #example_answer = squidpy_rag.run(query, chat_history)
    #final_answer = example_answer + "\n\nPlease modify the code based on the current context and use `python_repl_tool` to run the modified code above."
    
    return squidpy_rag.run(query, chat_history)
__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
