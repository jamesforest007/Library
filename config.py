import os

class Config:
    # Secret key for session management and security
    SECRET_KEY = 'your-secret-key'  # In production, use a secure random key
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///libraxo.db'  # Creates physical file libraxo.db
    
    # Disable SQLAlchemy modification tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    
    # Application settings
    FLASK_ENV = 'development'  # Set to 'production' in production
    DEBUG = True              # Disable in production
    
    # File upload settings
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size 