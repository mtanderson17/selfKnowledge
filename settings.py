import os  


class BaseConfig:
    """Base configuration"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False  
    SECRET_KEY = 'temp'
    DEBUG = True
    


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  
    DEBUG = True


class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    WTF_CSRF_ENABLED=False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')  


class ProductionConfig(BaseConfig):
    """Production configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  
    DEBUG = False
