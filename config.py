import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # ✅ use env var
    SQLALCHEMY_TRACK_MODIFICATIONS = False
