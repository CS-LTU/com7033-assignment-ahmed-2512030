from flask import Blueprint, jsonify, request
from app.models.patient import Patient
from app.utils.prediction import predict_stroke_risk
from flask_login import login_required

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/predict/<patient_id>', methods=['GET'])
@login_required
def get_prediction(patient_id):
    patient = Patient.get_by_id(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    
    try:
        prediction, probability = predict_stroke_risk(
            patient.age,
            patient.hypertension,
            patient.heart_disease,
            patient.avg_glucose_level,
            patient.bmi,
            patient.gender,
            patient.smoking_status
        )
        
        return jsonify({
            'patient_id': str(patient._id),
            'stroke_prediction': int(prediction),
            'stroke_probability': float(probability),
            'risk_level': "High" if probability > 0.5 else "Low"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
