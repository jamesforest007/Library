# Import necessary modules
from app import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin  # Add AnonymousUserMixin
from datetime import datetime
import pandas as pd
import io

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

    @classmethod
    def export_to_excel(cls):
        """
        Export all company data to an Excel file.
        """
        # Query all companies
        companies = cls.query.all()
        
        # Convert to DataFrame
        data = []
        for company in companies:
            company_dict = {}
            # Get all fields from the model
            for column in cls.__table__.columns:
                company_dict[column.name] = getattr(company, column.name)
            data.append(company_dict)
        
        df = pd.DataFrame(data)
        
        # Create Excel file in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Companies')
        
        output.seek(0)  # Go back to the start of the BytesIO object
        return output

    @classmethod
    def import_from_excel(cls, excel_file):
        """
        Import company data from an Excel file and completely overwrite the existing
        company records in the database.
        """
        # Read the Excel file
        df = pd.read_excel(excel_file)
        
        try:
            # Begin transaction
            # Delete all existing companies
            cls.query.delete()
            
            # Create new companies from Excel data
            for _, row in df.iterrows():
                # Convert row to dict
                data = row.to_dict()
                
                # Clean up the data
                for key, value in list(data.items()):
                    # Remove NaN values
                    if pd.isna(value):
                        data[key] = None
                        
                    # Convert timestamps to datetime objects if needed
                    if key == 'created_at' and value is not None:
                        try:
                            if isinstance(value, str):
                                data[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
                        except:
                            # If conversion fails, use current time
                            data[key] = datetime.utcnow()
                
                # Create new company record
                new_company = cls(**data)
                db.session.add(new_company)
                
            # Commit all changes
            db.session.commit()
            return True
        except Exception as e:
            # Roll back in case of error
            db.session.rollback()
            raise e 