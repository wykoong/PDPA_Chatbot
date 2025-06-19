import openai
from app.config import Config
from app.services.logger_service import chat_logger

class OpenAIService:
    """
    Service class for interacting with OpenAI's chat models.
    """
    def __init__(self) -> None:
        """
        Initializes the OpenAI client using API key and model name from configuration.
        """
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model_name = Config.OPENAI_API_MODEL

    def generate_response(self, prompt: str) -> str:
        """
        Generate a response from the OpenAI chat model based on the user's prompt.
        Logs any errors or exceptions to the exception log.

        Args:
            prompt (str): The user's input prompt.

        Returns:
            str: The AI-generated response from the model.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content
            if content is None:
                return "[No response generated]"
            return content
        except Exception as e:
            chat_logger.log_exception(f"OpenAI API error: {e}")
            return "[Error: Unable to generate response]"
