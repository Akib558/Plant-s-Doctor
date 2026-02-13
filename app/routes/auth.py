from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services import auth_service, email_service
from app.utils.validators import validate_email
from app.utils.decorators import login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login.html')
@auth_bp.route('/login')
def login():
    """Render login page"""
    if 'user_id' in session:
        return redirect(url_for('main.home'))
    return render_template('login.html')

@auth_bp.route('/login_validation', methods=['POST'])
def login_validation():
    """Handle login form submission"""
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    
    if not email or not password:
        flash('Email and password are required.', 'danger')
        return render_template('login.html')
    
    user = auth_service.authenticate_user(email, password)
    
    if user:
        session['user_id'] = user.id
        session['name'] = user.username
        session['email'] = user.email
        session['prediction_credits'] = user.prediction_credits
        session['is_admin'] = user.is_admin
        
        flash(f'Welcome back, {user.username}!', 'success')
        return render_template('ppp.html', name=user.username)
    else:
        flash('Invalid email or password.', 'danger')
        return render_template('login.html')

@auth_bp.route('/registation')
@auth_bp.route('/register')
def register():
    """Render registration page"""
    return render_template('reg.html')

@auth_bp.route('/reg_user', methods=['POST'])
def reg_user():
    """Handle user registration"""
    username = request.form.get('uname', '').strip()
    email = request.form.get('uemail', '').strip()
    password = request.form.get('upassword', '')
    
    if not username or not email or not password:
        flash('All fields are required.', 'danger')
        return render_template('reg.html')
    
    if not validate_email(email):
        flash('Invalid email format.', 'danger')
        return render_template('reg.html')
    
    from app.services.user_service import get_user_by_email
    if get_user_by_email(email):
        flash('Email already registered.', 'danger')
        return render_template('reg.html')
    
    user = auth_service.create_user(username, email, password)
    
    session['user_id'] = user.id
    session['name'] = user.username
    session['email'] = user.email
    session['prediction_credits'] = user.prediction_credits
    session['is_admin'] = user.is_admin
    
    flash('Registration successful!', 'success')
    return redirect(url_for('main.home'))

@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    from app.services.user_service import get_user_by_id, update_user_credits
    
    user_id = session.get('user_id')
    credits = session.get('prediction_credits', 0)
    
    if user_id:
        user = get_user_by_id(user_id)
        if user:
            user.prediction_credits = credits
            from app import db
            db.session.commit()
    
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgot_page')
def forgot_page():
    """Render forgot password page"""
    return render_template('forgot.html')

@auth_bp.route('/forgot', methods=['POST', 'GET'])
def forgot():
    """Handle forgot password request"""
    if 'user_id' in session:
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        if not email:
            flash('Email is required.', 'danger')
            return render_template('forgot.html')
        
        token = auth_service.create_password_reset_token(email)
        
        if token:
            email_service.send_password_reset_email(email, token)
            flash('Password reset token sent to your email.', 'success')
            return redirect(url_for('auth.reset'))
        else:
            flash('Email not found.', 'danger')
    
    return render_template('forgot.html')

@auth_bp.route('/reset', methods=['GET', 'POST'])
def reset():
    """Render password reset page"""
    return render_template('reset.html')

@auth_bp.route('/reset_fun', methods=['POST', 'GET'])
def reset_fun():
    """Handle password reset"""
    token = request.form.get('token', '').strip()
    password = request.form.get('password', '')
    cpassword = request.form.get('cpassword', '')
    
    if not token or not password or not cpassword:
        flash('All fields are required.', 'danger')
        return render_template('reset.html')
    
    if password != cpassword:
        flash('Passwords do not match.', 'danger')
        return render_template('reset.html')
    
    if auth_service.reset_password(token, password):
        flash('Password reset successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    else:
        flash('Invalid or expired token.', 'danger')
        return render_template('reset.html')

@auth_bp.route('/change_password', methods=['POST', 'GET'])
@login_required
def change_password():
    """Handle password change"""
    main_password = request.form.get('main_password', '')
    new_password = request.form.get('new_password', '')
    con_password = request.form.get('con_password', '')
    
    if not main_password or not new_password or not con_password:
        flash('All fields are required.', 'danger')
        return redirect(url_for('main.change_password_page'))
    
    if new_password != con_password:
        flash('New passwords do not match.', 'danger')
        return redirect(url_for('main.change_password_page'))
    
    if auth_service.change_user_password(session['user_id'], main_password, new_password):
        flash('Password changed successfully!', 'success')
        return redirect(url_for('main.user_profile'))
    else:
        flash('Current password is incorrect.', 'danger')
        return redirect(url_for('main.change_password_page'))

@auth_bp.route('/check_token', methods=['POST'])
@login_required
def check_token():
    """Handle credit token redemption"""
    token_val = request.form.get('token_val', '').strip()
    
    if not token_val:
        flash('Token is required.', 'danger')
        return redirect(url_for('main.user_profile'))
    
    if auth_service.redeem_credit_token(token_val, session['user_id']):
        session['prediction_credits'] = session.get('prediction_credits', 0) + 1000
        flash('Credit token redeemed successfully! 1000 credits added.', 'success')
    else:
        flash('Invalid or expired token.', 'danger')
    
    return redirect(url_for('main.user_profile'))

@auth_bp.route('/increase_token')
@login_required
def increase_token():
    """Generate and send credit increase token"""
    token = auth_service.create_credit_token(session['email'])
    
    if token:
        email_service.send_credit_token_email(session['email'], token)
        flash('Credit token sent to your email.', 'success')
    else:
        flash('Error generating token.', 'danger')
    
    return redirect(url_for('main.get_token_inc_page'))
