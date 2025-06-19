import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the application."""
    # Required configurations
    SECRET_KEY: str = os.getenv('SECRET_KEY', '')
    GEMINI_API_KEY: str = os.environ.get("GEMINI_API_KEY", "")
    GEMINI_API_URL: str = os.environ.get("GEMINI_API_URL", "")
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
    OPENAI_API_MODEL: str = os.environ.get("OPENAI_API_MODEL", "gpt-4.1-nano")

    # Optional configurations with default values
    MAX_REQUESTS_PER_MINUTE: int = int(os.getenv('MAX_REQUESTS_PER_MINUTE', '60'))
    REQUEST_TIMEOUT: int = int(os.getenv('REQUEST_TIMEOUT', '10'))
    MAX_OUTPUT_TOKENS: int = int(os.getenv('MAX_OUTPUT_TOKENS', '8192'))

    # GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    # GOOGLE_CLOUD_LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    # GOOGLE_CLOUD_MODEL = os.environ.get("GOOGLE_CLOUD_MODEL", "gemini-pro")

    @classmethod
    def validate(cls) -> None:
        """Validate required configuration values."""
        if not all([cls.GEMINI_API_KEY, cls.GEMINI_API_URL, cls.SECRET_KEY]):
            raise ValueError("Missing required environment variables")

# Validate configuration on import
Config.validate()

# Allowed keywords for topic validation
ALLOWED_KEYWORDS = [
    "personal data privacy", "data protection", "data privacy", "privacy law", "GDPR", "PDPA",
    "ai governance", "AI governance", "AI ethics", "AI law", "AI regulation", "artificial intelligence governance",
    "compliance", "data subject", "personal data", "data protection act", "privacy regulation",
    "data protection best practices", "data subject rights", "compliance requirements"
]

# Welcome message
WELCOME_MESSAGE = """Hello! I'm your AI PDPA assistant. I can help you with questions about:
- Personal Data Protection Act (PDPA)
- Data privacy regulations
- Data protection best practices
- Compliance requirements
- Data subject rights

How can I assist you today?"""

# Irrelevant topic response
IRRELEVANT_RESPONSE = """I apologize, but I can only assist with questions related to:
- Personal Data Protection Act (PDPA)
- Data privacy regulations
- Data protection best practices
- Compliance requirements
- Data subject rights

Please rephrase your question to focus on these topics."""

# Gemini model configuration
GEMINI_CONFIG = {
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 2048
}
