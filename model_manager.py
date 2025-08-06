"""
Model Manager - Handles switching between OpenAI and OpenRouter
"""
import os
import yaml
from openai import OpenAI
from loguru import logger
from typing import Dict, Any, Optional

class ModelManager:
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the model manager with configuration."""
        self.config = self._load_config(config_path)
        self.provider = self.config.get("model_provider", "openai")
        self.client = self._initialize_client()
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found. Using defaults.")
            return {"model_provider": "openai"}
            
    def _initialize_client(self) -> OpenAI:
        """Initialize the appropriate client based on provider."""
        if self.provider == "openrouter":
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                logger.error("OPENROUTER_API_KEY not found in environment")
                raise ValueError("OPENROUTER_API_KEY environment variable is required")
                
            base_url = self.config.get("openrouter", {}).get("base_url", "https://openrouter.ai/api/v1")
            logger.info(f"Using OpenRouter with base URL: {base_url}")
            
            return OpenAI(
                api_key=api_key,
                base_url=base_url,
                default_headers={
                    "HTTP-Referer": os.getenv("YOUR_SITE_URL", "http://localhost"),
                    "X-Title": "SDR Email Generator"
                }
            )
        else:
            # Default to OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                logger.error("OPENAI_API_KEY not found in environment")
                raise ValueError("OPENAI_API_KEY environment variable is required")
                
            logger.info("Using OpenAI API")
            return OpenAI(api_key=api_key)
            
    def get_model_name(self) -> str:
        """Get the configured model name."""
        if self.provider == "openrouter":
            return self.config.get("openrouter", {}).get("model", "anthropic/claude-3-sonnet")
        else:
            return self.config.get("openai", {}).get("model", "gpt-4-turbo-preview")
            
    def get_temperature(self) -> float:
        """Get the configured temperature."""
        provider_config = self.config.get(self.provider, {})
        return provider_config.get("temperature", 0.7)
        
    def get_max_tokens(self) -> int:
        """Get the configured max tokens."""
        provider_config = self.config.get(self.provider, {})
        return provider_config.get("max_tokens", 2000)
        
    def create_completion(self, messages: list, model: Optional[str] = None, **kwargs) -> Any:
        """Create a chat completion with error handling."""
        model = model or self.get_model_name()
        temperature = kwargs.get("temperature", self.get_temperature())
        max_tokens = kwargs.get("max_tokens", self.get_max_tokens())
        
        try:
            logger.debug(f"Creating completion with model: {model}")
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response
        except Exception as e:
            logger.error(f"Error creating completion: {str(e)}")
            raise
            
    def list_available_models(self) -> list:
        """List available models for the current provider."""
        if self.provider == "openrouter":
            return self.config.get("openrouter", {}).get("available_models", [])
        else:
            return ["gpt-4-turbo-preview", "gpt-4", "gpt-3.5-turbo"]