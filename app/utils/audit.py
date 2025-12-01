from flask import request, current_app
from flask_login import current_user
from datetime import datetime

def log_audit(action, details=None):
    """
    Logs an action to the audit_logs collection in MongoDB.
    """
    if not current_user.is_authenticated:
        user_id = "Anonymous"
        username = "Anonymous"
    else:
        user_id = current_user.id
        username = current_user.username

    log_entry = {
        'timestamp': datetime.utcnow(),
        'user_id': user_id,
        'username': username,
        'ip_address': request.remote_addr,
        'action': action,
        'details': details or {},
        'endpoint': request.endpoint,
        'method': request.method
    }

    try:
        db = current_app.db_mongo
        db.audit_logs.insert_one(log_entry)
    except Exception as e:
        current_app.logger.error(f"Failed to write audit log: {e}")
