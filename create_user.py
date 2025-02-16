from app import create_app, db
from app.models import User, TEAM_CHOICES
from werkzeug.security import generate_password_hash
from random import choice

def create_test_users():
    app = create_app()
    with app.app_context():
        # Create admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                password=generate_password_hash('admin123'),
                teams='All Teams',  # Admin has access to all teams
                is_active=True,
                is_admin=True
            )
            db.session.add(admin)
            print("Admin user created:")
            print("Username: admin")
            print("Password: admin123")
            print("-------------------")

        # Create 10 regular users
        for i in range(1, 11):
            username = f'user{i}'
            if not User.query.filter_by(username=username).first():
                user = User(
                    username=username,
                    password=generate_password_hash(f'password{i}'),
                    teams=choice(TEAM_CHOICES),  # Random team assignment as single team
                    is_active=True,
                    is_admin=False
                )
                db.session.add(user)
                print(f"Regular user created:")
                print(f"Username: {username}")
                print(f"Password: password{i}")
                print(f"Team: {user.teams}")
                print("-------------------")

        db.session.commit()
        print("All users created successfully!")

if __name__ == '__main__':
    create_test_users() 