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
    Talisman(app, 
             content_security_policy=app.config['CSP'], 
             force_https=app.config['FORCE_HTTPS']
    )

    # Initialize MongoDB
    # We attach it to app for easy access, or use a global client if preferred
    app.mongo_client = MongoClient(app.config['MONGO_URI'])
    app.db_mongo = app.mongo_client.get_database()

    # Register Blueprints
    from app.auth.routes import auth
    from app.patients.routes import patients
    from app.api.routes import api_bp
    from app.home.routes import home
    
    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(patients, url_prefix='/patients')
    app.register_blueprint(api_bp)
    
    # Create DB tables
    with app.app_context():
        db.create_all()

    return app
