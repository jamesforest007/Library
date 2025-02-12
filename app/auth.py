from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db

# Create authentication blueprint
auth = Blueprint('auth', __name__)

# Login route - handles both GET and POST requests
@auth.route('/login', methods=['GET', 'POST'])
def login():
    print("Login route accessed")  # Debug print
    if request.method == 'POST':
        print("POST request received")  # Debug print
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Form data - Username: {username}, Password length: {len(password)}")  # Debug print
        
        # Debug print
        print(f"Login attempt - Username: {username}")
        
        # Check if user exists
        user = User.query.filter_by(username=username).first()
        if not user:
            flash('Username not found.')
            return render_template('login.html')
            
        # Check password
        if check_password_hash(user.password, password):
            login_user(user)
            print(f"Login successful for user: {username}")
            return redirect(url_for('main.index'))
        else:
            flash('Incorrect password.')
        
    return render_template('login.html')

# Logout route
@auth.route('/logout')
@login_required  # User must be logged in to access this route
def logout():
    logout_user()  # Log out the user
    return redirect(url_for('auth.login'))  # Redirect to login page 