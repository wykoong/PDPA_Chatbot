# AI PDPA Assistant

A WhatsApp-like chat interface for interacting with an AI assistant specialized in Personal Data Protection Act (PDPA) and data privacy topics.

This Python program is developed using Cursor with 100% AI coding. 

## Features

- 🤖 AI-powered responses using Google's Gemini, OpenAI, or LangChain models
- 💬 WhatsApp-like chat interface
- 📝 Markdown support for formatted responses
- 🔍 Topic validation to ensure relevant discussions
- 📚 Conversation history tracking (with context-aware prompt formatting)
- 📊 Comprehensive logging system
- 🔄 Easily switch between AI providers via configuration
- 🧠 Automatic prompt length management to comply with model token limits

## Project Structure

```
app/
├── services/
│   ├── logger_service.py         # Logging functionality
│   ├── conversation_service.py   # Conversation history management and context formatting
│   ├── gemini_service.py         # Gemini AI integration (with history and prompt length logic)
│   ├── openai_service.py         # OpenAI integration
│   └── langchain_service.py      # LangChain integration
├── utils/
│   ├── utils.py                  # Utility functions
│   └── validators.py             # Input validation
├── static/
│   ├── css/
│   │   └── style.css             # WhatsApp-like styling
│   └── js/
│       └── chat.js               # Chat interface functionality
├── templates/
│   └── index.html                # Main chat interface
├── config.py                     # Configuration settings
├── __main__.py                   # Module entry point
└── app.py                        # Main application file
```

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd AI_PDPA
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env`
   - Update the values in `.env` with your API keys for Gemini, OpenAI, and Flask as needed

5. Run the application:
```bash
python -m app
```

## Configuration

The application can be configured through `config.py` and environment variables:

- `ALLOWED_KEYWORDS`: List of keywords for topic validation
- `WELCOME_MESSAGE`: Initial greeting message
- `IRRELEVANT_RESPONSE`: Message for off-topic questions
- `GEMINI_CONFIG`: Gemini model configuration settings
- `OPENAI_API_KEY`, `OPENAI_API_MODEL`: OpenAI API credentials and model
- `MAX_OUTPUT_TOKENS`: Maximum output tokens for AI responses (used for prompt length management)

## Features in Detail

### Multi-Provider AI Support
- Easily switch between Gemini, and OpenAI by changing the configuration.
- Each provider has its own service class for clean separation and maintainability.

### Topic Validation
The assistant only responds to questions related to:
- Personal Data Protection Act (PDPA)
- Data privacy regulations
- Data protection best practices
- Compliance requirements
- Data subject rights

### Conversation History & Context-Aware Prompts
- Maintains context of the last question and response.
- When generating a response, the assistant includes the previous question and answer in the prompt for better context.
- If the combined prompt (including history) exceeds half of `MAX_OUTPUT_TOKENS`, only the current question is sent to ensure compliance with model limits.

### Prompt Length Management
- The system automatically checks and trims the prompt to avoid exceeding model token limits, ensuring reliable operation.

### Logging
- Comprehensive logging of user messages and AI responses
- Error tracking and debugging support
- Separate logging service for better organization

### UI Features
- WhatsApp-like interface
- Markdown support for formatted responses
- Responsive design
- Maximizable chat window
- Loading indicators
- Error handling

## Development Notes

- Do **not** commit `__pycache__` directories or `.pyc` files. Add them to your `.gitignore` if not already present.
- Each service is modular and can be extended or replaced as needed.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.