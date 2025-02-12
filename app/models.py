# Import necessary modules
from app import db, login_manager
from flask_login import UserMixin  # Provides default implementations for Flask-Login interface
from datetime import datetime

# User model for authentication
class User(UserMixin, db.Model):
    # Database columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

# Required by Flask-Login to load user from database
@login_manager.user_loader
def load_user(user_id):
    # Convert user_id to integer and query database
    return User.query.get(int(user_id))

# Add to existing models.py
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100))
    category = db.Column(db.String(50))
    rack = db.Column(db.String(50))
    available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 