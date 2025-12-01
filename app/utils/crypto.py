from cryptography.fernet import Fernet
from flask import current_app

def get_fernet():
    key = current_app.config.get('ENCRYPTION_KEY')
    if not key:
        raise ValueError("ENCRYPTION_KEY not set in config")
    # Ensure key is bytes
    if isinstance(key, str):
        key = key.encode()
    return Fernet(key)

def encrypt_data(data):
    if data is None:
        return None
    f = get_fernet()
    return f.encrypt(str(data).encode()).decode()

def decrypt_data(token):
    if token is None:
        return None
    f = get_fernet()
    try:
        return f.decrypt(token.encode()).decode()
    except Exception:
        return None
