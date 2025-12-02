import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'RANDOM-SECRET-KEY'
    
    # SQLAlchemy
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MongoDB
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27018/stroke_app'

    # Security
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production' # Only True in prod with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Fernet key must be 32 url-safe base64-encoded bytes.
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY') or b'8co-7-z1x4-7-z1x4-7-z1x4-7-z1x4-7-z1x4-7-z1x4='

    # 2FA
    WTF_CSRF_ENABLED = True
    
    # Talisman
    FORCE_HTTPS = os.environ.get('FLASK_ENV') == 'production'
    
    # Content Security Policy
    CSP = {
        'default-src': "'self'",
        'script-src': ["'self'", 'https://cdn.tailwindcss.com', 'https://cdnjs.cloudflare.com', 'https://cdn.jsdelivr.net', "'unsafe-inline'"],
        'style-src': ["'self'", 'https://cdn.tailwindcss.com', 'https://cdnjs.cloudflare.com', 'https://fonts.googleapis.com', 'https://cdn.jsdelivr.net', "'unsafe-inline'"],
        'font-src': ["'self'", 'https://fonts.gstatic.com', 'https://cdnjs.cloudflare.com'],
        'img-src': ["'self'", 'data:', 'https://*'],
    }
