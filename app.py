import os
from app import create_app, db
from app.models import User, Prediction, PasswordResetToken, CreditToken

app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Make database models available in flask shell"""
    return {
        'db': db,
        'User': User,
        'Prediction': Prediction,
        'PasswordResetToken': PasswordResetToken,
        'CreditToken': CreditToken
    }

@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print("Database initialized!")

@app.cli.command()
def create_admin():
    """Create admin user"""
    from app import bcrypt
    
    username = input("Enter admin username: ")
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    
    user = User.query.filter_by(email=email).first()
    if user:
        print("User already exists!")
        return
    
    admin = User(
        username=username,
        email=email,
        password_hash=bcrypt.generate_password_hash(password).decode('utf-8'),
        is_admin=True,
        prediction_credits=99999
    )
    
    db.session.add(admin)
    db.session.commit()
    
    print(f"Admin user '{username}' created successfully!")

if __name__ == '__main__':
    app.run(port=5001, debug=True)
