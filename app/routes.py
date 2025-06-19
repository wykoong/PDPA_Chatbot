from flask import Blueprint, request, jsonify, render_template, current_app
from functools import wraps
import markdown2
from app.services.rate_limiter import RateLimiter
from app.services.gemini_service import GeminiService
from app.utils.validators import is_in_scope
from app.config import Config, WELCOME_MESSAGE
from app.services.langchain_service import LangChainService
import app.config as config
from app.services.logger_service import chat_logger

main_bp = Blueprint('main', __name__)
rate_limiter = RateLimiter(Config.MAX_REQUESTS_PER_MINUTE, 60)

# project = Config.GOOGLE_CLOUD_PROJECT
# location = Config.GOOGLE_CLOUD_LOCATION
# model = Config.GOOGLE_CLOUD_MODEL

def rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not rate_limiter.is_allowed():
            return jsonify({"response": "Rate limit exceeded. Please try again later."}), 429
        return f(*args, **kwargs)
    return decorated_function

def validate_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({"response": "Request must be JSON"}), 400
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({"response": "Missing 'question' in request"}), 400
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")

@main_bp.route("/api/chat", methods=["POST"])
@rate_limit
@validate_request
def chat():
    """Handle chat requests."""
    try:
        data = request.get_json()
        question = data.get("question", "").strip()
        
        chat_logger.log_user_message(question)  # Log user input

        if not is_in_scope(question):
            return jsonify({
                "response": "I can only answer questions about personal data privacy or AI governance. Please ask a relevant question."
            }), 400

        answer = GeminiService.get_response(question)
        if not answer:
            chat_logger.log_exception(f"App-level error: {e}")
            return jsonify({"response": "Sorry, there was an error processing your request."}), 500

        chat_logger.log_ai_response(answer)  # Log AI response

        formatted_answer = markdown2.markdown(answer, extras=["fenced-code-blocks", "tables"])
        return jsonify({"response": formatted_answer}), 200
    except Exception as e:
        chat_logger.log_exception(f"Error in /chat route: {e}")
        return jsonify({"response": "Sorry, there was an error processing your request."}), 500

@main_bp.route('/langchain', methods=['POST'])
def langchain_generate():
    data = request.get_json()
    prompt = data.get('prompt')
    provider = data.get('provider', 'gemini')

    chat_logger.log_user_message(f"[{provider}] {prompt}")

    if not prompt:
        error_msg = "Prompt is missing in the request."
        chat_logger.log_exception(f"App-level error: {e}")
        return jsonify({'error': 'Prompt is required'}), 400

    try:
        service = LangChainService(provider=provider)
        response = service.generate_response(prompt)
        chat_logger.log_ai_response(str(response))
        formatted_response = markdown2.markdown(
            response,
            extras=["fenced-code-blocks", "tables", "break-on-newline"]
        )
        return jsonify({'response': formatted_response})
    except Exception as e:
        chat_logger.log_exception(f"Exception in /langchain: {str(e)}")
        return jsonify({'error': str(e)}), 500

@main_bp.route('/welcome', methods=['GET'])
def welcome():
    formatted_welcome = markdown2.markdown(
        WELCOME_MESSAGE,
        extras=["fenced-code-blocks", "tables", "break-on-newline"]
    )
    return jsonify({'response': formatted_welcome})
