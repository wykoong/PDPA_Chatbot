"""
Service for managing conversation history and formatting prompts with context.
"""

from typing import Optional, Dict

class ConversationService:
    """
    Manages conversation history and prompt formatting for context-aware responses.
    """

    def __init__(self) -> None:
        """
        Initialize the conversation history.
        """
        self.history: Dict[str, Optional[str]] = {
            'last_question': None,
            'last_response': None
        }
    
    def format_prompt_with_history(self, current_question: str) -> str:
        """
        Format the prompt to include previous question and response for context.

        Args:
            current_question (str): The current user question.

        Returns:
            str: The formatted prompt including history if available.
        """
        if self.history['last_question'] and self.history['last_response']:
            return (
                f"Previous question: {self.history['last_question']}\n"
                f"Previous response: {self.history['last_response']}\n\n"
                f"Current question: {current_question}"
            )
        return current_question
    
    def update_history(self, question: str, response: str) -> None:
        """
        Update the conversation history with a new question and response.

        Args:
            question (str): The latest user question.
            response (str): The latest AI response.
        """
        self.history['last_question'] = question
        self.history['last_response'] = response
    
    def clear_history(self) -> None:
        """
        Clear the conversation history.
        """
        self.history['last_question'] = None
        self.history['last_response'] = None

# Create a singleton instance
conversation_service = ConversationService() 