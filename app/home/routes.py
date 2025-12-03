from flask import Blueprint, render_template, current_app
from flask_login import login_required
from datetime import datetime, timedelta

home = Blueprint('home', __name__)

@home.route('/')
@home.route('/index')
@login_required
def index():
    db = current_app.db_mongo
    
    # Get total patients count
    total_patients = db.patients.count_documents({})
    
    # Get high risk cases (patients with stroke predictions > 50%)
    # This requires checking audit logs for predictions
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Count assessments today from audit logs
    assessments_today = db.audit_logs.count_documents({
        'action': 'predict_stroke',
        'timestamp': {'$gte': today_start}
    })
    
    # Get high risk count from audit logs where risk > 50%
    # Use aggregation to get latest prediction per patient, then count high risk
    pipeline = [
        {'$match': {'action': 'predict_stroke'}},
        {'$sort': {'timestamp': -1}},  # Sort by timestamp descending
        {'$group': {
            '_id': '$details.patient_id',  # Group by patient_id
            'latest_risk': {'$first': '$details.risk'},  # Get first (latest) risk
            'latest_timestamp': {'$first': '$timestamp'}
        }},
        {'$match': {'latest_risk': {'$gt': 50}}}  # Filter for high risk
    ]
    
    high_risk_patients = list(db.audit_logs.aggregate(pipeline))
    high_risk_count = len(high_risk_patients)
    
    return render_template('home/index.html', 
                         title='Dashboard',
                         total_patients=total_patients,
                         high_risk_count=high_risk_count,
                         assessments_today=assessments_today)

