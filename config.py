import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-this-key-secure-random-string'
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27018/stroke_app'

    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY') or 'iJkN6XPB2A6vGQPIUqd-zr1Jfz6XQ7mnuoqQc66feME='

    WTF_CSRF_ENABLED = True
    
    FORCE_HTTPS = os.environ.get('FLASK_ENV') == 'production'
    
    CSP = {
        'default-src': "'self'",
        'script-src': ["'self'", 'https://cdn.tailwindcss.com', 'https://cdnjs.cloudflare.com', 'https://cdn.jsdelivr.net', "'unsafe-inline'"],
        'style-src': ["'self'", 'https://cdn.tailwindcss.com', 'https://cdnjs.cloudflare.com', 'https://fonts.googleapis.com', 'https://cdn.jsdelivr.net', "'unsafe-inline'"],
        'font-src': ["'self'", 'https://fonts.gstatic.com', 'https://cdnjs.cloudflare.com'],
        'img-src': ["'self'", 'data:', 'https://*'],
    }
