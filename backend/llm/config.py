"""
LLM Configuration Module
Provides shared LLM setup and utilities.
"""

import logging
from typing import Optional
from langchain_groq import ChatGroq

from backend.core.config import get_settings

logger = logging.getLogger(__name__)


class LLMConfig:
    # Configuration and factory for LLM instances
    
    DEFAULT_MODEL = "llama-3.1-8b-instant"
    DEFAULT_TEMPERATURE = 0.1
    
    @staticmethod
    def resolve_api_key(api_key: Optional[str] = None) -> Optional[str]:
        # Resolve API key from parameter or settings, returns resolved API key or None
        if api_key:
            return api_key
        
        try:
            settings = get_settings()
            return settings.groq_api_key
        except Exception as e:
            logger.warning(f"Could not get API key from settings: {e}")
            return None
    
    @staticmethod
    def create_llm(
        api_key: Optional[str] = None,
        model_name: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE
    ) -> Optional[ChatGroq]:
        # Create a ChatGroq LLM instance with specified parameters, returns LLM instance or None if failed
        resolved_key = LLMConfig.resolve_api_key(api_key)
        
        if not resolved_key:
            logger.warning("No GROQ_API_KEY found in settings or parameters")
            return None
        
        try:
            llm = ChatGroq(
                groq_api_key=resolved_key,
                model_name=model_name,
                temperature=temperature,
            )
            logger.info(f"LLM initialized successfully with model: {model_name}")
            return llm
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            return None
    
    @staticmethod
    def is_llm_available(api_key: Optional[str] = None) -> bool:
        # Check if LLM is available, returns True if LLM can be initialized
        try:
            from langchain_groq import ChatGroq
            
            resolved_key = LLMConfig.resolve_api_key(api_key)
            return resolved_key is not None
        except ImportError:
            logger.warning("langchain_groq not available")
            return False


# Convenience functions
def get_llm(
    api_key: Optional[str] = None,
    model_name: str = LLMConfig.DEFAULT_MODEL,
    temperature: float = LLMConfig.DEFAULT_TEMPERATURE
) -> Optional[ChatGroq]:
    # Get an LLM instance with specified parameters, returns LLM instance or None if failed
    return LLMConfig.create_llm(api_key, model_name, temperature)


def is_llm_available(api_key: Optional[str] = None) -> bool:
    # Check if LLM is available, returns True if LLM can be initialized
    return LLMConfig.is_llm_available(api_key)

