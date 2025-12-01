import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-this-key-secure-random-string'
    
    # SQLAlchemy
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MongoDB
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27018/stroke_app'

    # Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    # Fernet key must be 32 url-safe base64-encoded bytes.
    # Generate with: from cryptography.fernet import Fernet; Fernet.generate_key()
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY') or b'8co-7-z1x4-7-z1x4-7-z1x4-7-z1x4-7-z1x4-7-z1x4=' # Replace in prod!

    
    # 2FA
    WTF_CSRF_ENABLED = True
