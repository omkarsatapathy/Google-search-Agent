import os
from langchain_openai import ChatOpenAI

class LLMFactory:
    """Factory for creating language model instances"""
    
    @staticmethod
    def create_llm(provider, ollama_class=None, ollama_available=False):
        """Create and return a language model based on the specified provider
        
        Args:
            provider: The LLM provider ("OpenAI" or "Local (Ollama)")
            ollama_class: The Ollama class to use if provider is "Local (Ollama)"
            ollama_available: Whether Ollama is available
            
        Returns:
            LLM instance or None if creation failed
        """
        if provider == "OpenAI":
            if not os.getenv("OPENAI_API_KEY"):
                return None
            return ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
        else:  # Local (Ollama)
            if not ollama_available:
                return None
            
            try:
                return ollama_class(model="gemma3:4b")
            except Exception:
                return None