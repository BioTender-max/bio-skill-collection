# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

from agents.Biomaster import Biomaster
from langchain_core.messages import HumanMessage
import yaml
import json
import os
import sys

# Load configuration from YAML file
def load_config(config_path='config.yaml'):
    """Load YAML configuration file"""
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

# Main function
if __name__ == "__main__":
    # Parse command line arguments to get config file path
    config_path = sys.argv[1] if len(sys.argv) > 1 else 'config.yaml'
    
    # If config file doesn't exist, report error and exit
    if not os.path.exists(config_path):
        print(f"Error: Configuration file '{config_path}' does not exist")
        sys.exit(1)
    
    # Load configuration
    config = load_config(config_path)
    
    # Get API settings from configuration
    api_key = config['api']['main']['key']
    base_url = config['api']['main']['base_url']
    embedding_api_key = config['api']['embedding']['key']
    embedding_base_url = config['api']['embedding']['base_url']
    
    # Ollama settings
    use_ollama = config.get('biomaster', {}).get('use_ollama', False)
    ollama_config = config.get('api', {}).get('ollama', {})
    ollama_enabled = ollama_config.get('enabled', False)
    # Use ollama if specified in both biomaster and ollama sections
    use_ollama = use_ollama and ollama_enabled
    ollama_base_url = ollama_config.get('base_url', 'http://localhost:11434')
    
    # Get model settings from configuration
    Model = config['models']['main']
    tool_model = config['models'].get('tool', Model)  # Use main model if tool model not specified
    embedding_model = config['models']['embedding']
    
    # Get Biomaster settings from configuration
    excutor = config['biomaster']['executor']
    ids = config['biomaster']['id']
    generate_plan = config['biomaster'].get('generate_plan', True)  # Default to True
    
    # Get data and goal from configuration
    datalist = config['data']['files']
    goal = config['data']['goal']

    print(f"Using ollama: {use_ollama}")
    print(f"Ollama base URL: {ollama_base_url}")
    print(f"Model: {Model}")
    print(f"Embedding model: {embedding_model}")

    # Initialize Biomaster instance
    manager = Biomaster(
        api_key, 
        base_url,
        excutor=excutor,
        id=ids,
        Model=Model,
        embedding_model=embedding_model,
        tool_model=tool_model,
        embedding_base_url=embedding_base_url,
        embedding_api_key=embedding_api_key,
        use_ollama=use_ollama,
        ollama_base_url=ollama_base_url
    )
    
    # If using ollama, test connection
    if use_ollama:
        print("Testing Ollama connection...")
        if not manager.test_ollama_connection():
            print("Warning: Unable to connect to ollama service or model not found. Continuing in API mode.")
            manager.use_ollama = False
        else:
            print(f"Successfully connected to Ollama service, using model: {manager.ollama_model} and embedding model: {manager.ollama_embedding_model}")

    # Execute PLAN based on configuration
    if generate_plan:
        manager.execute_PLAN(goal, datalist)
        print("**********************************************************")

    # Execute TASK
    PLAN_results_dict = manager.execute_TASK(datalist)
    print(PLAN_results_dict)

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
