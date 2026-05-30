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
import base64
from datetime import datetime
import matplotlib.pyplot as plt
from typing import Annotated, TypedDict, Literal, Tuple, List
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph
from langgraph.graph.message import AnyMessage, add_messages
#from langchain_experimental.utilities import PythonREPL
from tools import PythonREPL
from langgraph.prebuilt import ToolNode
from prompt import system_prompt
from langgraph.types import Command
from textwrap import dedent
import streamlit as st
from util import display_message, render_conversation_history, get_conversation_summary
from langchain_core.runnables.config import RunnableConfig
from tools import google_scholar_search, squidpy_rag_agent, visualize_cell_cell_interaction_tool, visualize_spatial_cell_type_map, visualize_cell_type_composition, visualize_umap, report_tool
# Directory Setup
plot_dir = os.path.join(os.path.dirname(__file__), "tmp/plots")
os.makedirs(plot_dir, exist_ok=True)
load_dotenv()

python_repl = PythonREPL()

@tool(response_format="content_and_artifact")
def python_repl_tool(query: str) -> Tuple[str, List[str]]:
    """A Python shell. Use this to execute python commands. Input should be a valid python command. 
    If you want to see the output of a value, you should print it out with `print(...)`. """
    
    plot_paths = []  # List to store file paths of generated plots
    result_parts = []  # List to store different parts of the output
    
    try:
        output = python_repl.run(query)
        if output and output.strip():
            result_parts.append(output.strip())
        
        figures = [plt.figure(i) for i in plt.get_fignums()]
        if figures:
            for fig in figures:
                fig.set_size_inches(10, 6)  # Ensure figures are large enough
                #fig.tight_layout()  # Prevent truncation# Generate filename
                plot_filename = f"plot_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"
                # Create relative path
                rel_path = os.path.join("tmp/plots", plot_filename)
                # Convert to absolute path for saving
                abs_path = os.path.join(os.path.dirname(__file__), rel_path)
                
                fig.savefig(abs_path,bbox_inches='tight')
                plot_paths.append(rel_path)  # Store relative path
            
            plt.close("all")
            result_parts.append(f"Generated {len(plot_paths)} plot(s).")
        
        if not result_parts:  # If no output and no figures
            result_parts.append("Executed code successfully with no output. If you want to see the output of a value, you should print it out with `print(...)`.")

    except Exception as e:
        result_parts.append(f"Error executing code: {e}")
    
    # Join all parts of the result with newlines
    result_summary = "\n".join(result_parts)
    
    # Return both the summary and plot paths (if any)
    return result_summary, plot_paths

# Tools List and Node Setup
tools = [
    python_repl_tool,
    google_scholar_search,
    squidpy_rag_agent,
    visualize_cell_cell_interaction_tool,
    visualize_spatial_cell_type_map,
    visualize_cell_type_composition,
    visualize_umap,
    report_tool
]
tool_node = ToolNode(tools)

# Graph Setup
class GraphsState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    input_messages_len: list[int]
graph = StateGraph(GraphsState)

gpt_4o = ChatOpenAI(model_name="gpt-4o", temperature=0).bind_tools(tools, parallel_tool_calls=False)


models = {
    "gpt-4o": gpt_4o
}

def _call_model(state: GraphsState, config: RunnableConfig) -> Command[Literal["tools", "__end__"]]:
    st.session_state["final_state"]["messages"]=state["messages"]
    model_name = config["configurable"].get("model", "gpt-4o")
    llm = models[model_name]
    previous_message_count = len(state["messages"])
    state["input_messages_len"].append(previous_message_count)
    render_conversation_history(state["messages"][state["input_messages_len"][-2]:state["input_messages_len"][-1]])
    cur_messages_len = len(state["messages"])-state["input_messages_len"][0]  
    if cur_messages_len > 200:
        st.markdown(
        f"""
        <p style="color:blue; font-size:16px;">
            Current recursion step is {cur_messages_len}. Terminated because you exceeded the limit of 200.
        </p>
        """,
        unsafe_allow_html=True
        )
        st.session_state["render_last_message"] = False
        return Command(
        update={"messages": []},
        goto="__end__",
    )
    last_message = state["messages"][-1]
# Check if last message is a ToolMessage and has artifacts
    if isinstance(last_message, ToolMessage) and hasattr(last_message, "artifact") and last_message.artifact and model_name != "gpt-3.5-turbo":
        # Prepare content list with initial text
        content_list = [{
            "type": "text",
            "text": """
                Please analyze these generated images by the code above. Your tasks are to:
                1. Examine each visualization carefully
                2. Provide a detailed description of what you observe
                3. Explain the biological implications of the observations if any.
                4. You should use google scholar to find more information to see if the literature supports your observation. 
                5. please always do multiple search queries (at least 5) to get a better understanding of the observation.
                6. After you finish your writing, please continue to the next steps according to the system instructions. unless user shows intention for interaction or you are not sure about the next step.
                7. Remember to be consistent with the user's input language. you are a multi-lingual assistant.
                8. If you don't see any plots, or the plots are not clear or crowded, please try to fix the code. if you want to see the plots then don't use plt.close"
            """
        }]
        
        # Add all PNG images to the content list
        for rel_path in last_message.artifact:
            if rel_path.endswith(".png"):
                # Convert relative path to absolute based on current script location
                abs_path = os.path.join(os.path.dirname(__file__), rel_path)
                if os.path.exists(abs_path):
                    with open(abs_path, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode("utf-8")
                    content_list.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image_data}"}
                    })
        
        # Create a single message with all images if we found any
        if len(content_list) > 1:  # Only if we have at least one image
            image_message = HumanMessage(content=content_list,name="image_assistant")
            state["messages"].append(image_message)
            
    response = llm.invoke(state["messages"])
    if response.tool_calls:
        return Command(
        update={"messages": [response]},
        goto="tools",
    )
    else:
        st.session_state["render_last_message"] = True
        return Command(
        update={"messages": [response]},
        goto="__end__",
    )

graph.add_edge(START, "modelNode")
graph.add_node("tools", tool_node)
graph.add_node("modelNode", _call_model)
graph.add_edge("tools", "modelNode")
graph_runnable = graph.compile()
def invoke_our_graph(messages,model_choose):
    config = {"recursion_limit": 200, "configurable": {"model": model_choose}}
    return graph_runnable.invoke({"messages": messages,"input_messages_len":[len(messages)]},config=config)

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
