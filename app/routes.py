from flask import Blueprint, request, jsonify, render_template
from functools import wraps
import markdown2
from app.services.rate_limiter import RateLimiter
from app.services.gemini_service import GeminiService
from app.utils.validators import is_in_scope
from app.config import Config

main_bp = Blueprint('main', __name__)
rate_limiter = RateLimiter(Config.MAX_REQUESTS_PER_MINUTE, 60)

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
    data = request.get_json()
    question = data.get("question", "").strip()
    
    if not is_in_scope(question):
        return jsonify({
            "response": "I can only answer questions about personal data privacy or AI governance. Please ask a relevant question."
        }), 400

    answer = GeminiService.get_response(question)
    if not answer:
        return jsonify({"response": "Sorry, I couldn't process your request. Please try again."}), 500

    formatted_answer = markdown2.markdown(answer, extras=["fenced-code-blocks", "tables"])
    return jsonify({"response": formatted_answer}), 200
