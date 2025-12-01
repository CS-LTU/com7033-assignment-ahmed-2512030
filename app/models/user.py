from app.extensions import db, login_manager
from flask_login import UserMixin
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    totp_secret = db.Column(db.String(32)) # For 2FA
    is_2fa_enabled = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = ph.hash(password)

    def check_password(self, password):
        try:
            return ph.verify(self.password_hash, password)
        except VerifyMismatchError:
            return False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
