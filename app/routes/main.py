from flask import Blueprint, render_template, session, redirect, url_for
from app.utils.decorators import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """Home page"""
    if 'user_id' in session:
        return render_template('ppp.html', name=session['name'])
    return redirect(url_for('auth.login'))

@main_bp.route('/ppp.html')
@login_required
def ppp():
    """Main dashboard page"""
    return render_template('ppp.html', name=session['name'])

@main_bp.route('/apple.html')
@login_required
def apple():
    """Apple prediction page"""
    if session.get('name') == 'admin' or session.get('is_admin'):
        return render_template('apple_a.html')
    return render_template('apple.html')

@main_bp.route('/tomato.html')
@login_required
def tomato():
    """Tomato prediction page"""
    if session.get('name') == 'admin' or session.get('is_admin'):
        return render_template('tomato_a.html')
    return render_template('tomato.html')

@main_bp.route('/potato.html')
@login_required
def potato():
    """Potato prediction page"""
    if session.get('name') == 'admin' or session.get('is_admin'):
        return render_template('potato_a.html')
    return render_template('potato.html')

@main_bp.route('/rice.html')
@login_required
def rice():
    """Rice prediction page"""
    if session.get('name') == 'admin' or session.get('is_admin'):
        return render_template('rice_a.html')
    return render_template('rice.html')

@main_bp.route('/user_profile')
@login_required
def user_profile():
    """User profile page"""
    return render_template(
        'user_profile.html',
        name=session['name'],
        email=session['email'],
        count=session.get('prediction_credits', 0)
    )

@main_bp.route('/change_password_page')
@login_required
def change_password_page():
    """Change password page"""
    return render_template('change_password.html')

@main_bp.route('/get_token_inc_page')
@login_required
def get_token_inc_page():
    """Token increase page"""
    return render_template('get_token.html')

@main_bp.route('/trial_page')
def trial_page():
    """Trial page"""
    return render_template('trial.html')
