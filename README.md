# AI PDPA Assistant

A WhatsApp-like chat interface for interacting with an AI assistant specialized in Personal Data Protection Act (PDPA) and data privacy topics.

This Python program is developed using Cursor with 100% AI coding. 

## Features

- 🤖 AI-powered responses using Google's Gemini model
- 💬 WhatsApp-like chat interface
- 📝 Markdown support for formatted responses
- 🔍 Topic validation to ensure relevant discussions
- 📚 Conversation history tracking
- 📊 Comprehensive logging system

## Project Structure

```
app/
├── services/
│   ├── logger_service.py    # Logging functionality
│   └── conversation_service.py  # Conversation history management
├── static/
│   ├── css/
│   │   └── style.css       # WhatsApp-like styling
│   └── js/
│       └── chat.js         # Chat interface functionality
├── templates/
│   └── index.html         # Main chat interface
├── config.py              # Configuration settings
└── app.py                # Main application file
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
   - Update the values in `.env` with your keys

5. Run the application:
```bash
python app/app.py
```

## Configuration

The application can be configured through `config.py`:

- `ALLOWED_KEYWORDS`: List of keywords for topic validation
- `WELCOME_MESSAGE`: Initial greeting message
- `IRRELEVANT_RESPONSE`: Message for off-topic questions
- `GEMINI_CONFIG`: AI model configuration settings

## Features in Detail

### Topic Validation
The assistant only responds to questions related to:
- Personal Data Protection Act (PDPA)
- Data privacy regulations
- Data protection best practices
- Compliance requirements
- Data subject rights

### Conversation History
- Maintains context of the last question and response
- Improves response relevance and continuity
- Helps in maintaining conversation flow

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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.