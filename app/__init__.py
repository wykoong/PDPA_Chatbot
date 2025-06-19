from flask import Flask
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
from app.config import Config
from app.services.logger_service import chat_logger

def create_app() -> Flask:
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask app.
    """
    try:
        app = Flask(__name__,
                    template_folder='templates',  # Specify template folder
                    static_folder='static')       # Specify static folder
        
        CORS(app)
        
        # Load configuration
        app.config.from_object(Config)
        
        # Initialize extensions
        toolbar = DebugToolbarExtension(app)
        
        # Register blueprints
        from app.routes import main_bp
        app.register_blueprint(main_bp)
        
        # Log successful initialization (to exception log as per your request)
        chat_logger.log_exception("Flask app initialized and blueprints registered successfully.")
        
        # Remove printing of routes/paths
        # for rule in app.url_map.iter_rules():
        #     print(rule)
        
        return app
    except Exception as e:
        chat_logger.log_exception(f"Error during Flask app initialization: {e}")
        raise

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

