# Import necessary Flask extensions and modules
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # For database operations
from flask_login import LoginManager    # For handling user authentication
from config import DevelopmentConfig, ProductionConfig
from flask_debugtoolbar import DebugToolbarExtension

# Initialize Flask extensions
db = SQLAlchemy()  # Database instance
login_manager = LoginManager()  # Login manager instance
toolbar = DebugToolbarExtension()

def create_app():
    # Create Flask application instance
    app = Flask(__name__)
    # Choose config based on environment
    config = DevelopmentConfig if os.environ.get('FLASK_ENV') == 'development' else ProductionConfig
    app.config.from_object(config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Set login view for unauthorized users
    login_manager.login_view = 'auth.login'
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from app.routes import main
    from app.auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth)
    
    return app 