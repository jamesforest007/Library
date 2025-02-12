from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def create_test_user():
    app = create_app()
    with app.app_context():
        # Check if user already exists
        if not User.query.filter_by(username='admin').first():
            user = User(
                username='admin',
                password=generate_password_hash('admin123'),
                is_active=True
            )
            db.session.add(user)
            db.session.commit()
            print("Test user created successfully!")
            print("Username: admin")
            print("Password: admin123")
        else:
            print("Test user already exists!")

if __name__ == '__main__':
    create_test_user() 