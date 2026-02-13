from app import db
from app.models import User

def get_user_by_id(user_id):
    """Get user by ID"""
    return User.query.get(user_id)

def get_user_by_email(email):
    """Get user by email"""
    return User.query.filter_by(email=email).first()

def update_user_credits(user_id, credits_change):
    """Update user's prediction credits"""
    user = User.query.get(user_id)
    if user:
        user.prediction_credits += credits_change
        db.session.commit()
        return user.prediction_credits
    return None

def deduct_prediction_credit(user_id):
    """Deduct one prediction credit from user"""
    return update_user_credits(user_id, -1)
