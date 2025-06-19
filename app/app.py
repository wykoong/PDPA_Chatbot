from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv
from app.services.logger_service import chat_logger
from app.services.conversation_service import conversation_service
import markdown2
from app.config import ALLOWED_KEYWORDS, WELCOME_MESSAGE, GEMINI_CONFIG, IRRELEVANT_RESPONSE
import app.routes  # This ensures routes are registered

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash-lite')

# Configure generation config
generation_config = genai.types.GenerationConfig(
    temperature=GEMINI_CONFIG['temperature'],
    top_p=GEMINI_CONFIG['top_p'],
    top_k=GEMINI_CONFIG['top_k'],
    max_output_tokens=GEMINI_CONFIG['max_output_tokens'],
)

app = Flask(__name__)

def create_app() -> Flask:
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask app.
    """
    app = Flask(__name__)
    # ... config ...
    # If using blueprints, register them here
    return app

def is_relevant_question(message: str) -> bool:
    """
    Check if the question is related to PDPA and data privacy topics.

    Args:
        message (str): The user's message.

    Returns:
        bool: True if relevant, False otherwise.
    """
    message_lower = message.lower()
    return any(keyword.lower() in message_lower for keyword in ALLOWED_KEYWORDS)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    
    # Log the user's message
    chat_logger.log_user_message(message)
    
    try:
        # Check if the question is relevant
        if not is_relevant_question(message):
            response_text = IRRELEVANT_RESPONSE
        else:
            # Format prompt with conversation history
            prompt = conversation_service.format_prompt_with_history(message)
            
            # Generate response using Gemini with specific configuration
            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            # Get the response text
            response_text = response.text
            
            # Update conversation history
            conversation_service.update_history(message, response_text)
        
        # Convert markdown to HTML
        formatted_response = markdown2.markdown(
            response_text,
            extras=["fenced-code-blocks", "tables", "break-on-newline"]
        )
        
        # Log the AI's response
        chat_logger.log_ai_response(response_text)
        
    except Exception as e:
        error_message = f"Error generating response: {str(e)}"
        print(error_message)
        chat_logger.log_exception(f"App-level error: {e}")
        formatted_response = "I apologize, but I encountered an error while processing your request. Please try again."
    
    return jsonify({'response': formatted_response})

@app.route('/welcome', methods=['GET'])
def welcome():
    # Convert welcome message markdown to HTML
    formatted_welcome = markdown2.markdown(
        WELCOME_MESSAGE,
        extras=["fenced-code-blocks", "tables", "break-on-newline"]
    )
    return jsonify({'response': formatted_welcome})

if __name__ == '__main__':
    app.run(debug=True) 