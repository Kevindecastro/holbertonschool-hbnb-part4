import os
from datetime import timedelta  # Add this import


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')  # Ensure SECRET_KEY is set for security
    DEBUG = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'Voicimonsecret')  # Secret key for JWT
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Expiry time for the access token

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'  # SQLite database (use appropriate URI for other DBs)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
