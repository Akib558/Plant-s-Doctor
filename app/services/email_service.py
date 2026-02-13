from flask import current_app
from flask_mail import Message
from app import mail

def send_password_reset_email(email, token):
    """Send password reset email with token"""
    msg = Message(
        "Password Reset Request",
        recipients=[email]
    )
    msg.body = f"""To reset your password, please use the following token:

{token}

This token will expire in 1 hour.

If you did not request a password reset, please ignore this email.
"""
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_credit_token_email(email, token):
    """Send credit increase token email"""
    msg = Message(
        "Prediction Credits Token",
        recipients=[email]
    )
    msg.body = f"""Your prediction credits token:

{token}

Use this token to increase your prediction credits by 1000.

This token will expire in 24 hours.
"""
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
