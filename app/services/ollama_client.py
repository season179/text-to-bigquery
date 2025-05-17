import os
from typing import Dict, Optional, Any, List

import ollama
import requests
from pydantic import BaseModel

from app.config import OLLAMA_MODEL, OLLAMA_HOST, OLLAMA_TIMEOUT

class OllamaResponse(BaseModel):
    response: str
    model: str
    created_at: str
    done: bool
    context: Optional[List[int]] = None
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_count: Optional[int] = None
    prompt_eval_duration: Optional[int] = None
    eval_count: Optional[int] = None
    eval_duration: Optional[int] = None

class OllamaClient:
    """Client for interacting with Ollama API to generate SQL from natural language."""
    
    def __init__(
        self,
        model_name: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
    ):
        """
        Initialize the Ollama client.
        
        Args:
            model_name: The name of the model to use (default from config)
            base_url: The base URL of the Ollama API (default from config)
            timeout: Request timeout in seconds (default from config)
        """
        self.model_name = model_name or OLLAMA_MODEL
        self.base_url = base_url or OLLAMA_HOST
        self.timeout = timeout or OLLAMA_TIMEOUT
        
        # Set base URL for ollama library
        ollama.client._base_url = self.base_url
    
    def generate_sql(self, prompt: str) -> str:
        """
        Generate SQL from natural language using the Ollama API.
        
        Args:
            prompt: The natural language prompt to convert to SQL
            
        Returns:
            The generated SQL query as a string
        
        Raises:
            Exception: If the API call fails
        """
        try:
            # Generate response using ollama client library
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": 0.1,  # Lower temperature for more deterministic SQL generation
                }
            )
            
            if isinstance(response, dict) and "response" in response:
                return response["response"]
            return str(response)
        
        except Exception as e:
            # Log the error and re-raise
            print(f"Error generating SQL with Ollama: {str(e)}")
            raise

    def health_check(self) -> bool:
        """
        Check if Ollama API is available and the model is loaded.
        
        Returns:
            True if the API is reachable and the model is available, False otherwise
        """
        try:
            # Try to hit the Ollama API list endpoint to check if it's up
            response = requests.get(f"{self.base_url}/api/tags", timeout=self.timeout)
            response.raise_for_status()
            
            # Check if the model is in the list of available models
            models = response.json().get("models", [])
            for model in models:
                if model.get("name") == self.model_name:
                    return True
                
            # If the model isn't loaded, return False
            return False
        
        except Exception as e:
            # Log the error and return False
            print(f"Error checking Ollama health: {str(e)}")
            return False