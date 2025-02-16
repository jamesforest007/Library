import os
from datetime import timedelta

class Config:
    # Base configuration
    DEBUG = False
    TESTING = False
    ENV = 'production'  # Default to production
    
    # Secret key for session management and CSRF protection
    SECRET_KEY = 'dev-secret-key'  # Default secret key
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///libraxo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    
    # Custom configuration
    ITEMS_PER_PAGE = 10
    UPLOAD_FOLDER = 'uploads'
    
    # Application settings
    FLASK_ENV = 'development'  # Set to 'production' in production
    DEBUG = True              # Disable in production
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size 
    
    # Session settings
    SESSION_PROTECTION = 'strong'
    
    # Proxy settings
    PROXY_PORT = 80

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    # Debug Toolbar settings
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True
    DEBUG_TB_PROFILER_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable in production
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Use stronger secret key if available, otherwise use default
    SECRET_KEY = os.environ.get('SECRET_KEY') or Config.SECRET_KEY