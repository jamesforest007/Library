# Import necessary Flask extensions and modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # For database operations
from flask_login import LoginManager    # For handling user authentication
from config import Config

# Initialize Flask extensions
db = SQLAlchemy()  # Database instance
login_manager = LoginManager()  # Login manager instance

def create_app():
    # Create Flask application instance
    app = Flask(__name__)
    # Load configuration from Config class
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    # Set the login view for unauthorized users
    login_manager.login_view = 'auth.login'

    # Create database tables within app context
    with app.app_context():
        from app import models  # Import models here
        db.create_all()        # Creates tables if they don't exist

    # Register blueprints (modular components of the app)
    from app.routes import main    # Import the main blueprint
    from app.auth import auth      # Import the auth blueprint
    
    app.register_blueprint(main)   # Register main routes (handles /)
    app.register_blueprint(auth)   # Register auth routes (handles /login, /logout)

    return app 