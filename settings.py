import os

SECRET_KEY = 'temp'
DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']