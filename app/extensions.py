from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymongo import MongoClient
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address)
csrf = CSRFProtect()
mongo_client = None # Will be initialized in create_app
