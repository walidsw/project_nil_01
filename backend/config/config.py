import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB max file size
    MODEL_PATH = os.getenv('MODEL_PATH', 'models/')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'dcm'}  # DICOM files
    
    # CORS settings
    CORS_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:*').split(',')
    
    # Model configurations
    IMAGE_SIZE = (224, 224)
    CONFIDENCE_THRESHOLD = 0.7

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}