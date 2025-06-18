class ConversationService:
    def __init__(self):
        self.history = {
            'last_question': None,
            'last_response': None
        }
    
    def format_prompt_with_history(self, current_question):
        """Format the prompt to include conversation history."""
        if self.history['last_question'] and self.history['last_response']:
            return f"""Previous question: {self.history['last_question']}
Previous response: {self.history['last_response']}

Current question: {current_question}"""
        return current_question
    
    def update_history(self, question, response):
        """Update the conversation history with new question and response."""
        self.history['last_question'] = question
        self.history['last_response'] = response
    
    def clear_history(self):
        """Clear the conversation history."""
        self.history['last_question'] = None
        self.history['last_response'] = None

# Create a singleton instance
conversation_service = ConversationService() 