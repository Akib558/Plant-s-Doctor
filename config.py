import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24).hex()
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://OQmAQgAGIs:OTh3lb0dWY@remotemysql.com/OQmAQgAGIs'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 465))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')
    
    # Upload Settings
    UPLOAD_FOLDER = os.path.join(basedir, os.environ.get('UPLOAD_FOLDER', 'uploads'))
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # ML Model Paths
    MODEL_PATH_TOMATO = os.path.join(basedir, 'all_models/tomato_model_inception.h5')
    MODEL_PATH_APPLE = os.path.join(basedir, 'all_models/apple_model.h5')
    MODEL_PATH_POTATO = os.path.join(basedir, 'all_models/potato_model.h5')
    MODEL_PATH_RICE = os.path.join(basedir, 'all_models/rice_model2.h5')
    MODEL_PATH_ERROR = os.path.join(basedir, 'all_models/error_model.h5')
    MODEL_PATH_ERROR_2 = os.path.join(basedir, 'all_models/error_model_2222.h5')
    
    # Application Settings
    DEFAULT_PREDICTION_CREDITS = int(os.environ.get('DEFAULT_PREDICTION_CREDITS', 10))

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_ECHO = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
