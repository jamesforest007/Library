# Import necessary modules
from app import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin  # Add AnonymousUserMixin
from datetime import datetime

# Add is_administrator to anonymous users
class Anonymous(AnonymousUserMixin):
    def is_administrator(self):
        return False

# Set anonymous user
login_manager.anonymous_user = Anonymous

# Define team choices
TEAM_CHOICES = ['Entertainment', 'Industrial', 'Financial']
ALL_TEAMS = 'All Teams'

# User model for authentication
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    # Database columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)  # Add admin role
    teams = db.Column(db.String(200))  # Store teams as comma-separated string

    def is_administrator(self):
        return self.is_admin

    def same_team(self, company):
        user_teams = self.teams.split(',') if self.teams else []
        return self.is_admin or company.teams in user_teams or ALL_TEAMS in user_teams

    @property
    def team_list(self):
        """Return teams as a list"""
        return self.teams.split(',') if self.teams else []

# Required by Flask-Login to load user from database
@login_manager.user_loader
def load_user(user_id):
    # Convert user_id to integer and query database
    return User.query.get(int(user_id))

# Add to existing models.py
class Company(db.Model):
    __tablename__ = 'company'  # Optional: specify table name
    
    # These define the columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    teams = db.Column(db.String(50))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    sector = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    location = db.Column(db.String(100))
    contact_person = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    status = db.Column(db.String(50), default='Active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 