from flask import Flask
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension
from app.config import Config

def create_app():
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
    
    return app
