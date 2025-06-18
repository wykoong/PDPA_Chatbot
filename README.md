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

2. **Run the app:**
   ```bash
   python app.py
   ```

3. **Open in browser:**
   Visit [http://localhost:5000](http://localhost:5000)

## File Structure
- `app.py` - Main Flask backend
- `templates/index.html` - Responsive chat frontend
- `requirements.txt` - Python dependencies

## Security Note
- The Gemini API key is hardcoded for demo purposes. For production, use environment variables or a secure vault. 