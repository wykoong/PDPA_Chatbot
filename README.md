# Gemini 2.0 Flash-Lite Chatbot

A Flask-based chatbot web app using Gemini 2.0 Flash-Lite model, restricted to questions about personal data privacy and AI governance.

Thsi Python program is developed using Cursor with 100% AI coding. 

## Features
- Responsive web UI (Bootstrap)
- Gemini 2.0 Flash-Lite API integration
- Only answers questions about personal data privacy or AI governance
- Rejects out-of-scope questions


## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   - Copy `.env.example` to `.env`
   - Update the values in `.env` with your API keys

3. **Run the app:**
   ```bash
   # Method 1: Using run.py (Recommended)
   python run.py

   # Method 2: Using Flask CLI
   export FLASK_APP=run.py
   export FLASK_DEBUG=1
   flask run
   ```

4. **Open in browser:**
   Visit [http://localhost:5000](http://localhost:5000)

## File Structure
- `run.py` - Application entry point
- `app/` - Main application package
  - `__init__.py` - App factory and initialization
  - `config.py` - Configuration settings
  - `routes.py` - Route definitions
  - `services/` - Business logic
    - `gemini_service.py` - Gemini API integration
    - `rate_limiter.py` - Rate limiting implementation
  - `utils/` - Utility functions
    - `validators.py` - Input validation
  - `static/` - Static files
    - `css/style.css` - Custom styles
    - `js/app.js` - Vue.js application
- `templates/` - HTML templates
  - `index.html` - Main page template
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (API keys and configuration)
- `README.md` - Project documentation

## Security Note
- API keys and sensitive configuration are stored in `.env` file
- Add `.env` to `.gitignore` to prevent committing sensitive data
- For production, use a secure vault or environment variables management system 

## .env file
- following info are configured in the file
GEMINI_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent
GEMINI_API_KEY="GEMINI_API_KEY"
SECRET_KEY="SECRET_KEY"

- Remember to replace all above value