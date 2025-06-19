"""
Service for handling language model responses using different providers (OpenAI, Gemini).
"""

import requests
from app.config import Config
from app.services.openai_service import OpenAIService
from app.services.gemini_service import GeminiService
from app.services.logger_service import chat_logger

class LangChainService:
    """
    Service to generate responses using either OpenAI or Gemini as the provider.
    Logs any errors or exceptions to the exception log.
    """

    def __init__(self, provider: str = "gemini") -> None:
        """
        Initialize the LangChainService with the specified provider.

        Args:
            provider (str): The name of the provider ("openai" or "gemini").
        """
        self.provider = provider.lower()
        if self.provider == "openai":
            self.service = OpenAIService()
        else:
            self.api_url = Config.GEMINI_API_URL
            self.api_key = Config.GEMINI_API_KEY

    def generate_response(self, prompt: str) -> str | None:
        """
        Generate a response using the selected provider.

        Args:
            prompt (str): The user's input prompt.

        Returns:
            str | None: The generated response, or None if unavailable.
        """
        try:
            if self.provider == "openai":
                return self.service.generate_response(prompt)
            else:
                return GeminiService.get_response(prompt)
        except Exception as e:
            chat_logger.log_exception(f"LangChainService error: {e}")
            return None
