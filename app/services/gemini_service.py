import requests
from typing import Optional
from app.config import Config
from app.utils.utils import extract_gemini_response_text
from app.services.conversation_service import conversation_service
from app.services.logger_service import chat_logger

class GeminiService:
    """
    Service for interacting with the Gemini API, supporting conversation history.

    This service formats prompts to include the last user question and AI response,
    as long as the total prompt length does not exceed half of MAX_OUTPUT_TOKENS.
    If the prompt with history is too long, only the current question is sent.
    After receiving a response, the conversation history is updated.
    """

    @staticmethod
    def get_response(question: str) -> Optional[str]:
        """
        Get a response from the Gemini API, including conversation history if within token limit.

        The prompt is formatted to include the previous question and response for context.
        If the combined prompt exceeds half of MAX_OUTPUT_TOKENS (using character count as a proxy),
        only the current question is sent. After receiving a response, the conversation history
        is updated with the prompt and the response.

        Args:
            question (str): The user's current question.

        Returns:
            Optional[str]: The response text from Gemini, or None if there's an error.
        """
        # Format the prompt to include conversation history
        prompt_with_history = conversation_service.format_prompt_with_history(question)
        # Use character count as a proxy for token count
        max_prompt_length = Config.MAX_OUTPUT_TOKENS // 2

        # If the prompt with history is too long, use only the current question
        if len(prompt_with_history) > max_prompt_length:
            prompt_to_send = question
        else:
            prompt_to_send = prompt_with_history

        payload = {
            "contents": [{"parts": [{"text": prompt_to_send}]}],
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
            response_text = extract_gemini_response_text(response_data)
            # Update conversation history with the actual prompt sent and the response
            conversation_service.update_history(prompt_to_send, response_text)
            return response_text
        except requests.RequestException as e:
            chat_logger.log_exception(f"Gemini API error: {e}")
            return None
        except Exception as e:
            chat_logger.log_exception(f"Unexpected error in GeminiService: {e}")
            return None
