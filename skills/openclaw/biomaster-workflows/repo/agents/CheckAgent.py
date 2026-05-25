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
import json
import logging
import re
import requests
from typing import Dict, List, Tuple, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class CheckAgent:
    """
    CheckAgent, core functions:
    - Verify expected output files exist and are non-empty (0 bytes)
    - Scan directory and use LLM to identify possible output files when expected files don't exist
    - Update status in DEBUG_Output file
    """
    
    def __init__(self, api_key: str, base_url: str, model: str, 
                 use_ollama: bool = False, 
                 ollama_base_url: str = "http://localhost:11434",
                 ollama_model: str = "qwen3:32b"):
        # Set up logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        self.api_key = api_key
        self.base_url = base_url
        self.model = ChatOpenAI(model=model, base_url=base_url)
        self.use_ollama = use_ollama
        self.ollama_base_url = ollama_base_url
        self.ollama_model = ollama_model
        
        # Create prompt template
        self.file_prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are a bioinformatics file analysis expert. Based on the step information and file list,
            determine which files are likely valid outputs. Return JSON with:
            {{
                "analysis": "Detailed analysis of why files are valid or invalid",
                "output_filename": ["file1: description", "file2: description", ...],
                "stats": true/false (whether files are valid outputs)
            }}
            """),
            ("human", """
            Step details:
            - Step number: {step_number}
            - Tool: {tool_name}
            - Description: {step_description}
            
            Available files: {file_list}
            
            Expected output files: {expected_files}
            """)
        ])
    
    def check_file_size(self, file_path: str) -> Tuple[bool, str]:
        """Check if file exists and is not empty (0 bytes)"""
        if not os.path.exists(file_path):
            return False, f"File doesn't exist: {file_path}"
        
        if os.path.getsize(file_path) == 0:
            return False, f"File is empty (0 bytes): {file_path}"
            
        return True, f"File exists and has content"
    
    def scan_directory(self, directory: str) -> List[Dict[str, Any]]:
        """Scan all non-empty files in the directory"""
        if not os.path.exists(directory):
            return []
        
        files = []
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                path = os.path.join(root, filename)
                if os.path.exists(path) and os.path.getsize(path) > 0:
                    files.append({
                        "path": path,
                        "size": os.path.getsize(path)
                    })
        return files
    
    def get_step_details(self, task_id: str, step_number: str) -> Dict[str, Any]:
        """Get step details from PLAN.json"""
        plan_path = f"./output/{task_id}_PLAN.json"
        if not os.path.exists(plan_path):
            return {}
        
        try:
            with open(plan_path, 'r', encoding='utf-8') as plan_file:
                plan = json.load(plan_file)
                
            for step in plan.get("plan", []):
                if str(step.get("step_number", "")) == step_number:
                    return step
        except:
            return {}
        
        return {}
    
    def check_output_files(self, debug_output_path: str) -> Dict[str, Any]:
        """Check if output files declared in debug output actually exist"""
        
        # Read DEBUG output file
        try:
            with open(debug_output_path, 'r', encoding='utf-8') as f:
                debug_data = json.load(f)
                
            # Get declared output file list
            output_filenames = debug_data.get("output_filename", [])
            
            if not output_filenames:
                logging.warning(f"No output files declared in DEBUG output: {debug_output_path}")
                return {"stats": True, "analysis": "No output files declared"}
                
            # Files that actually exist
            existing_files = []
            missing_files = []
            
            for file_path in output_filenames:
                # Extract actual file path (may include description)
                if ":" in file_path:
                    file_path = file_path.split(":")[0].strip()
                    
                if os.path.exists(file_path):
                    existing_files.append(file_path)
                else:
                    missing_files.append(file_path)
                    
            # If all declared files exist
            if not missing_files:
                return {
                    "stats": True,
                    "analysis": f"All {len(existing_files)} output files exist",
                    "existing_files": existing_files,
                    "output_filename": output_filenames
                }
            
            # If some files are missing, provide analysis
            analysis = self._analyze_missing_files(debug_data, missing_files, existing_files)
            
            # Update stats field in DEBUG output file
            debug_data["stats"] = False
            debug_data["analyze"] = debug_data.get("analyze", "") + "\n\nFile verification failed: " + analysis
            
            with open(debug_output_path, 'w', encoding='utf-8') as f:
                json.dump(debug_data, f, indent=2, ensure_ascii=False)
                
            return {
                "stats": False, 
                "analysis": analysis,
                "missing_files": missing_files,
                "existing_files": existing_files,
                "output_filename": existing_files  # Only return files that actually exist
            }
            
        except Exception as e:
            logging.error(f"Error checking output files: {str(e)}")
            return {"stats": False, "analysis": f"Error during verification: {str(e)}"}
    
    def _analyze_missing_files(self, debug_data: Dict, missing_files: List[str], existing_files: List[str]) -> str:
        """Analyze reason for missing files"""
        
        # Extract script content and output
        shell_commands = debug_data.get("shell", [])
        result_output = debug_data.get("result", "")
        
        # Build analysis prompt
        if self.use_ollama:
            return self._analyze_with_ollama(shell_commands, result_output, missing_files, existing_files)
        else:
            return self._analyze_with_api(shell_commands, result_output, missing_files, existing_files)
            
    def _analyze_with_api(self, shell_commands, result_output, missing_files, existing_files):
        """Analyze missing files using API"""
        prompt = f"""
        Analyze the following Shell commands and execution results to explain why these files were not created:
        
        Missing files:
        {missing_files}
        
        Existing files:
        {existing_files}
        
        Shell commands:
        {shell_commands}
        
        Execution results:
        {result_output}
        
        Please analyze possible reasons.
        """
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a professional bioinformatics assistant skilled at analyzing Shell script execution issues."},
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis = result["choices"][0]["message"]["content"]
                return analysis
            else:
                logging.error(f"API response error: {response.status_code} - {response.text}")
                return f"Unable to analyze reason. API error: {response.status_code}"
        except Exception as e:
            logging.error(f"API request error: {str(e)}")
            return f"Unable to analyze reason. Request error: {str(e)}"
    
    def _analyze_with_ollama(self, shell_commands, result_output, missing_files, existing_files):
        """Analyze missing files using Ollama"""
        prompt = f"""
        Analyze the following Shell commands and execution results to explain why these files were not created:
        
        Missing files:
        {missing_files}
        
        Existing files:
        {existing_files}
        
        Shell commands:
        {shell_commands}
        
        Execution results:
        {result_output}
        
        Please analyze possible reasons.
        """
        
        system_prompt = "You are a professional bioinformatics assistant skilled at analyzing Shell script execution issues."
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.ollama_model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{self.ollama_base_url}/api/generate", 
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis = result.get("response", "")
                # Filter out thinking process
                analysis = re.sub(r'<think>.*?</think>', '', analysis, flags=re.DOTALL)
                return analysis
            else:
                logging.error(f"Ollama API error: {response.status_code} - {response.text}")
                return f"Unable to analyze reason. Ollama API error: {response.status_code}"
        except Exception as e:
            logging.error(f"Error requesting Ollama API: {str(e)}")
            return f"Unable to analyze reason. Request error: {str(e)}"

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
