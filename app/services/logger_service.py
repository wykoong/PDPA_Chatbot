import os
import logging
from datetime import datetime

class ChatLogger:
    """
    Logger for chat messages and exceptions.
    - chat_yyyymmdd.log: logs user/AI conversation.
    - exception_yyyymmdd.log: logs all errors, exceptions, and stack traces.
    """
    def __init__(self):
        self.chat_logger = self._setup_logger('chat', 'chat')
        self.exception_logger = self._setup_logger('exception', 'exception')

    def _setup_logger(self, logger_name: str, file_prefix: str) -> logging.Logger:
        """Set up and return a configured logger instance."""
        # Create logs directory if it doesn't exist
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Create logger
        current_date = datetime.now().strftime('%Y%m%d')
        log_file = os.path.join(log_dir, f'{file_prefix}_{current_date}.log')
        
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)

        # Create handler with custom file naming
        handler = logging.FileHandler(
            filename=log_file,
            encoding='utf-8',
            mode='a'  # append mode
        )

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)

        # Add handler to logger
        if not logger.handlers:
            logger.addHandler(handler)

        return logger

    def log_user_message(self, message: str) -> None:
        """Log a user message to the chat log."""
        self.chat_logger.info(f"User: {message}")

    def log_ai_response(self, response: str) -> None:
        """Log an AI response to the chat log."""
        self.chat_logger.info(f"AI: {response}")

    def log_exception(self, error_message: str) -> None:
        """Log an error or exception to the exception log, with stack trace."""
        self.exception_logger.error(error_message, exc_info=True)

# Create a singleton instance
chat_logger = ChatLogger() 