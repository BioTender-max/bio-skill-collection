# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.prompts import ChatPromptTemplate
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_community.document_loaders.text import TextLoader
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.tools import ShellTool
import os
from langchain_community.llms import Ollama
import requests
import json
import re

# JSON formatting prompt
_JSON_FORMAT_PROMPT = """You are a professional JSON formatting expert. Your task is to repair and format the following potentially malformed JSON string into valid JSON.
Ensure the output follows correct JSON format:
1. All keys must be enclosed in double quotes
2. String values must be enclosed in double quotes
3. Properly handle nested quotes, indentation, and escape characters
4. Ensure correct comma separation between array elements and object members
5. Remove any improperly formatted comments
6. Fix possible syntax errors

Please return only correctly formatted JSON, without any additional explanations or text.

Original JSON string:
{json_string}
"""

def Json_Format_Agent(json_string, api_key, base_url, tool_model="gpt-4o-mini", use_ollama=False, ollama_base_url="http://localhost:11434", ollama_model="qwen3:32b"):
    """
    Use LLM to repair and format JSON strings
    
    Parameters:
    - json_string: JSON string to format
    - api_key: OpenAI API key
    - base_url: API base URL
    - tool_model: Model name to use
    - use_ollama: Whether to use Ollama
    - ollama_base_url: Ollama API base URL
    - ollama_model: Ollama model name
    
    Returns:
    - Formatted JSON string
    """
    # Extract JSON part using regex
    json_match = re.search(r'```json\s*([\s\S]*?)\s*```', json_string)
    if json_match:
        json_string = json_match.group(1)
    
    # Try to parse JSON directly
    try:
        parsed_json = json.loads(json_string)
        return json.dumps(parsed_json, ensure_ascii=False)
    except json.JSONDecodeError:
        # If direct parsing fails, use LLM for repair
        pass
    
    if use_ollama:
        # Use Ollama for JSON formatting
        return _format_with_ollama(json_string, ollama_base_url, ollama_model)
    else:
        # Use OpenAI API for JSON formatting
        prompt = ChatPromptTemplate.from_template(_JSON_FORMAT_PROMPT)
        model = ChatOpenAI(temperature=0, model=tool_model, api_key=api_key, base_url=base_url)
        chain = prompt | model | StrOutputParser()
        corrected_json = chain.invoke({"json_string": json_string})
        return corrected_json

def _format_with_ollama(json_string, ollama_base_url, ollama_model):
    """Format JSON using Ollama"""
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "model": ollama_model,
        "prompt": f"Fix and format the following JSON string, return only properly formatted JSON:\n\n{json_string}",
        "system": "You are a professional JSON formatting expert. Please return only correctly formatted JSON, without any additional explanations or text.",
        "stream": False
    }
    
    try:
        response = requests.post(
            f"{ollama_base_url}/api/generate", 
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            formatted_text = result.get("response", "")
            
            # Filter out thinking process
            formatted_text = re.sub(r'<think>.*?</think>', '', formatted_text, flags=re.DOTALL)
            
            # Try to extract JSON part
            json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', formatted_text)
            if json_match:
                formatted_text = json_match.group(1)
            
            # Validate JSON
            try:
                parsed_json = json.loads(formatted_text)
                return json.dumps(parsed_json, ensure_ascii=False)
            except:
                # If not valid JSON, return original response
                return formatted_text
        else:
            return f"Ollama API error: {response.status_code}"
    except Exception as e:
        return f"Error requesting Ollama API: {str(e)}"
__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
