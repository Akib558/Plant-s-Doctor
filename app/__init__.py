import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
mail = Mail()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    from config import config
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    mail.init_app(app)
    
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    with app.app_context():
        from app.models import User, Prediction, PasswordResetToken, CreditToken
        
        from app.routes.auth import auth_bp
        from app.routes.main import main_bp
        from app.routes.prediction import prediction_bp
        
        app.register_blueprint(auth_bp)
        app.register_blueprint(main_bp)
        app.register_blueprint(prediction_bp)
    
    return app
