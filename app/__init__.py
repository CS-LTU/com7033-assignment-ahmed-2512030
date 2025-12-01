from flask import Flask
from flask_talisman import Talisman
from config import Config
from app.extensions import db, login_manager, limiter, csrf
from pymongo import MongoClient

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    limiter.init_app(app)
    csrf.init_app(app)
    
    # Talisman for security headers (HTTPS, CSP, etc.)
    # In development, we might want to disable force_https if running locally without SSL
    csp = {
        'default-src': '\'self\'',
        'script-src': ['\'self\'', 'https://cdn.jsdelivr.net'], # Allow Bootstrap/Tailwind CDN if needed
        'style-src': ['\'self\'', 'https://cdn.jsdelivr.net', '\'unsafe-inline\''],
    }
    Talisman(app, content_security_policy=csp, force_https=False) # Set force_https=True in prod

    # Initialize MongoDB
    # We attach it to app for easy access, or use a global client if preferred
    app.mongo_client = MongoClient(app.config['MONGO_URI'])
    app.db_mongo = app.mongo_client.get_database()

    # Register Blueprints
    from app.auth.routes import auth
    from app.patients.routes import patients
    from app.api.routes import api_bp
    
    app.register_blueprint(auth)
    app.register_blueprint(patients)
    app.register_blueprint(api_bp)
    
    # Create DB tables
    with app.app_context():
        db.create_all()

    return app
