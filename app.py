from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
import requests
import markdown2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Set the secret key from environment variable
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Enable debug mode
app.debug = True

# Initialize DebugToolbar
toolbar = DebugToolbarExtension(app)

# Get API keys from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = os.getenv('GEMINI_API_URL')

# Add validation
if not GEMINI_API_URL or not GEMINI_API_KEY:
    raise ValueError("Missing required environment variables: GEMINI_API_URL and/or GEMINI_API_KEY")

# Restriction keywords for allowed topics
ALLOWED_KEYWORDS = [
    "personal data privacy", "data protection", "data privacy", "privacy law", "GDPR", "PDPA",
    "ai governance", "AI governance", "AI ethics", "AI law", "AI regulation", "artificial intelligence governance"
]

@app.route("/")
def index():
    return render_template("index.html")

def is_in_scope(question: str) -> bool:
    q = question.lower()
    for keyword in ALLOWED_KEYWORDS:
        if keyword.lower() in q:
            return True
    return False

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "")
    if not is_in_scope(question):
        return jsonify({"response": "I can only answer questions about personal data privacy or AI governance. Please ask a relevant question."})

    payload = {
        "contents": [{"parts": [{"text": question}]}],
        "generationConfig": {
            "maxOutputTokens": 8192  # Increase token limit to 8,192
        }
    }
    params = {"key": GEMINI_API_KEY}
    try:
        resp = requests.post(GEMINI_API_URL, params=params, json=payload, timeout=10)
        resp.raise_for_status()
        gemini_response = resp.json()
        answer = gemini_response.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response from Gemini.")
        
        # Convert markdown to HTML
        formatted_answer = markdown2.markdown(answer, extras=["fenced-code-blocks", "tables"])
        return jsonify({"response": formatted_answer})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500

# Custom error handler
@app.errorhandler(Exception)
def handle_error(error):
    return jsonify({"response": f"An error occurred: {str(error)}"}), 500

if __name__ == "__main__":
    app.run(debug=True) 