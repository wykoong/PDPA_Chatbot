import os
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

class ChatLogger:
    def __init__(self):
        self.logger = self._setup_logger()

    def _setup_logger(self):
        # Create logs directory if it doesn't exist
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Create logger
        logger = logging.getLogger('chat_logger')
        logger.setLevel(logging.INFO)

        # Create handler with custom file naming
        current_date = datetime.now().strftime('%Y%m%d')
        log_file = os.path.join(log_dir, f'chat_{current_date}.log')
        
        handler = logging.FileHandler(
            filename=log_file,
            encoding='utf-8',
            mode='a'  # append mode
        )

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(handler)

        return logger

    def log_user_message(self, message):
        self.logger.info(f"User: {message}")

    def log_ai_response(self, response):
        self.logger.info(f"AI: {response}")

    def log_error(self, error_message):
        self.logger.error(f"Error: {error_message}")

# Create a singleton instance
chat_logger = ChatLogger() 