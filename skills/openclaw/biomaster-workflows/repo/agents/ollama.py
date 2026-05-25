# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

from langchain_community.llms import Ollama  # Import Ollama support
from langchain_core.embeddings import Embeddings
import os
import subprocess
import json
import re
import logging
from datetime import datetime
import uuid  # Used for generating unique IDs
import requests
import numpy as np
from typing import List

# Custom Ollama embedding model class
class OllamaEmbeddings(Embeddings):
    """Embedding model class using Ollama API"""
    
    def __init__(self, base_url: str, model: str):
        """
        Initialize Ollama embedding model
        
        Parameters:
        - base_url: Base URL for Ollama API
        - model: Name of the embedding model to use
        """
        self.base_url = base_url
        self.model = model
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Get embeddings for multiple texts
        
        Parameters:
        - texts: List of texts
        
        Returns:
        - List of embedding vectors
        """
        return [self.embed_query(text) for text in texts]
    
    def embed_query(self, text: str) -> List[float]:
        """
        Get embedding vector for a single query text
        
        Parameters:
        - text: Query text
        
        Returns:
        - Embedding vector
        """
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "prompt": text
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/embeddings", 
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                embedding = result.get("embedding", [])
                
                # Ensure the return value is a list of floats
                if embedding:
                    return [float(x) for x in embedding]
                else:
                    logging.error("Ollama API returned empty embedding vector")
                    # Return zero vector as fallback
                    return [0.0] * 1536  # Return 1536-dimensional zero vector
            else:
                logging.error(f"Ollama embedding API error: {response.status_code} - {response.text}")
                # Return zero vector as fallback
                return [0.0] * 1536
        except Exception as e:
            logging.error(f"Error requesting Ollama embedding API: {str(e)}")
            # Return zero vector as fallback
            return [0.0] * 1536
__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
