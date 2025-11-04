import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mysecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///patients.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
