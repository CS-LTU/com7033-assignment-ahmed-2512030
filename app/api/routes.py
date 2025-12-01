from flask import Blueprint
from flask_restx import Api, Resource, fields
from app.models.patient import Patient
from flask_login import login_required

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp, version='1.0', title='Stroke App API',
    description='A simple API for the Stroke Prediction App',
    doc='/docs'
)

ns = api.namespace('patients', description='Patient operations')

patient_model = api.model('Patient', {
    'first_name': fields.String(required=True, description='First Name'),
    'last_name': fields.String(required=True, description='Last Name'),
    'age': fields.Integer(required=True, description='Age'),
    'gender': fields.String(required=True, description='Gender'),
    'hypertension': fields.String(description='Hypertension (0/1)'),
    'heart_disease': fields.String(description='Heart Disease (0/1)'),
    'avg_glucose_level': fields.Float(description='Average Glucose Level'),
    'bmi': fields.Float(description='BMI'),
    'smoking_status': fields.String(description='Smoking Status'),
    'work_type': fields.String(description='Work Type'),
    'residence_type': fields.String(description='Residence Type')
})

@ns.route('/')
class PatientList(Resource):
    @ns.doc('list_patients')
    # @login_required # In a real API, use API Key or JWT. Skipping for demo simplicity or use session auth if browser-based
    def get(self):
        '''List all patients'''
        patients = Patient.get_all()
        return [p.to_dict() for p in patients]

    @ns.doc('create_patient')
    @ns.expect(patient_model)
    def post(self):
        '''Create a new patient'''
        data = api.payload
        patient = Patient(
            first_name=data['first_name'],
            last_name=data['last_name'],
            age=data['age'],
            gender=data['gender'],
            hypertension=data.get('hypertension', '0'),
            heart_disease=data.get('heart_disease', '0'),
            avg_glucose_level=data.get('avg_glucose_level', 0.0),
            bmi=data.get('bmi', 0.0),
            smoking_status=data.get('smoking_status', 'Unknown'),
            work_type=data.get('work_type', 'Private'),
            residence_type=data.get('residence_type', 'Urban')
        )
        patient_id = patient.save()
        return {'message': 'Patient created', 'id': str(patient_id)}, 201

@ns.route('/<string:id>')
@ns.response(404, 'Patient not found')
@ns.param('id', 'The patient identifier')
class PatientResource(Resource):
    @ns.doc('get_patient')
    def get(self, id):
        '''Fetch a patient given its identifier'''
        patient = Patient.get_by_id(id)
        if patient:
            return patient.to_dict()
        api.abort(404)
