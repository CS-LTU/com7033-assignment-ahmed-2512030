from app.models.patient import Patient
from app.utils.crypto import encrypt_data, decrypt_data

def test_encryption(app):
    original_data = "120.5"
    encrypted = encrypt_data(original_data)
    assert encrypted != original_data
    decrypted = decrypt_data(encrypted)
    assert decrypted == original_data

def test_patient_crud(client, app):
    # Clear any existing test data
    with app.app_context():
        app.db_mongo.patients.delete_many({})
        
    # Login first
    with app.app_context():
        from app import db
        from app.models.user import User
        u = User(username='testadmin', email='admin@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

    client.post('/login', data={'username': 'testadmin', 'password': 'password'}, follow_redirects=True)

    # Create Patient
    response = client.post('/patients/add', data={
        'first_name': 'John',
        'last_name': 'Doe',
        'age': 45,
        'gender': 'Male',
        'hypertension': '0',
        'heart_disease': '0',
        'avg_glucose_level': 105.5,
        'bmi': 28.5,
        'smoking_status': 'never smoked',
        'work_type': 'Private',
        'residence_type': 'Urban'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Patient added successfully' in response.data

    # Verify Patient was created
    with app.app_context():
        patients = Patient.get_all()
        assert len(patients) >= 1
        # Find our test patient
        john = next((p for p in patients if p.first_name == 'John' and p.last_name == 'Doe'), None)
        assert john is not None
        assert john.age == 45

