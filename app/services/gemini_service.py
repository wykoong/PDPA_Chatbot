import requests
from typing import Optional
from app.config import Config

class GeminiService:
    @staticmethod
    def get_response(question: str) -> Optional[str]:
        """
        Get response from Gemini API.
        
        Args:
            question: The user's question
            
        Returns:
            Optional[str]: The response text or None if there's an error
        """
        payload = {
            "contents": [{"parts": [{"text": question}]}],
            "generationConfig": {
                "maxOutputTokens": Config.MAX_OUTPUT_TOKENS
            }
        }
        params = {"key": Config.GEMINI_API_KEY}
        
        try:
            resp = requests.post(
                Config.GEMINI_API_URL,
                params=params,
                json=payload,
                timeout=Config.REQUEST_TIMEOUT
            )
            resp.raise_for_status()
            response_data = resp.json()
            
            candidates = response_data.get("candidates", [{}])
            if not candidates:
                return None
                
            content = candidates[0].get("content", {})
            parts = content.get("parts", [{}])
            if not parts:
                return None
                
            return parts[0].get("text")
        except requests.RequestException as e:
            return None
