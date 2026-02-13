import uuid
from datetime import datetime, timedelta
from app import db, bcrypt
from app.models import User, PasswordResetToken, CreditToken
from flask import current_app

def create_user(username, email, password):
    """Create a new user with hashed password"""
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        prediction_credits=current_app.config['DEFAULT_PREDICTION_CREDITS']
    )
    db.session.add(user)
    db.session.commit()
    return user

def authenticate_user(email, password):
    """Authenticate user by email and password"""
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        user.last_login = datetime.utcnow()
        db.session.commit()
        return user
    return None

def create_password_reset_token(email):
    """Generate password reset token for user"""
    user = User.query.filter_by(email=email).first()
    if not user:
        return None
    
    token_str = str(uuid.uuid4())
    token = PasswordResetToken(
        user_id=user.id,
        token=token_str,
        expires_at=datetime.utcnow() + timedelta(hours=1)
    )
    db.session.add(token)
    db.session.commit()
    return token_str

def verify_reset_token(token_str):
    """Verify password reset token validity"""
    token = PasswordResetToken.query.filter_by(token=token_str, used=False).first()
    if token and token.expires_at > datetime.utcnow():
        return token
    return None

def reset_password(token_str, new_password):
    """Reset user password using valid token"""
    token = verify_reset_token(token_str)
    if not token:
        return False
    
    user = User.query.get(token.user_id)
    user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
    token.used = True
    db.session.commit()
    return True

def change_user_password(user_id, old_password, new_password):
    """Change user password after verifying old password"""
    user = User.query.get(user_id)
    if not user or not bcrypt.check_password_hash(user.password_hash, old_password):
        return False
    
    user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
    db.session.commit()
    return True

def create_credit_token(email):
    """Generate credit increase token"""
    user = User.query.filter_by(email=email).first()
    if not user:
        return None
    
    token_str = str(uuid.uuid4())
    token = CreditToken(
        user_id=user.id,
        token=token_str,
        credits=1000,
        expires_at=datetime.utcnow() + timedelta(hours=24)
    )
    db.session.add(token)
    db.session.commit()
    return token_str

def redeem_credit_token(token_str, user_id):
    """Redeem credit token and add credits to user"""
    token = CreditToken.query.filter_by(token=token_str, used=False).first()
    if not token or token.expires_at < datetime.utcnow() or token.user_id != user_id:
        return False
    
    user = User.query.get(user_id)
    user.prediction_credits += token.credits
    token.used = True
    db.session.commit()
    return True
