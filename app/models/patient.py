from flask import current_app
from app.utils.crypto import encrypt_data, decrypt_data
from datetime import datetime
from bson import ObjectId

class Patient:
    def __init__(self, first_name, last_name, age, gender, hypertension, heart_disease, avg_glucose_level, bmi, smoking_status, work_type, residence_type, _id=None):
        self._id = _id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.hypertension = hypertension
        self.heart_disease = heart_disease
        self.avg_glucose_level = avg_glucose_level # Sensitive
        self.bmi = bmi # Sensitive
        self.smoking_status = smoking_status
        self.work_type = work_type
        self.residence_type = residence_type
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'gender': self.gender,
            'hypertension': self.hypertension,
            'heart_disease': self.heart_disease,
            'avg_glucose_level': encrypt_data(self.avg_glucose_level),
            'bmi': encrypt_data(self.bmi),
            'smoking_status': self.smoking_status,
            'work_type': self.work_type,
            'residence_type': self.residence_type,
            'created_at': self.created_at
        }

    @staticmethod
    def from_dict(data):
        if not data:
            return None
        return Patient(
            _id=data.get('_id'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            age=data.get('age'),
            gender=data.get('gender'),
            hypertension=data.get('hypertension'),
            heart_disease=data.get('heart_disease'),
            avg_glucose_level=decrypt_data(data.get('avg_glucose_level')),
            bmi=decrypt_data(data.get('bmi')),
            smoking_status=data.get('smoking_status'),
            work_type=data.get('work_type'),
            residence_type=data.get('residence_type')
        )

    @staticmethod
    def get_all(limit=20, skip=0, search_query=None):
        db = current_app.db_mongo
        query = {}
        if search_query:
            # Simple case-insensitive search on name
            query = {
                "$or": [
                    {"first_name": {"$regex": search_query, "$options": "i"}},
                    {"last_name": {"$regex": search_query, "$options": "i"}}
                ]
            }
        patients_data = db.patients.find(query).skip(skip).limit(limit)
        return [Patient.from_dict(p) for p in patients_data]

    @staticmethod
    def get_by_id(patient_id):
        db = current_app.db_mongo
        data = db.patients.find_one({'_id': ObjectId(patient_id)})
        return Patient.from_dict(data)

    def save(self):
        db = current_app.db_mongo
        data = self.to_dict()
        if self._id:
            db.patients.update_one({'_id': self._id}, {'$set': data})
        else:
            result = db.patients.insert_one(data)
            self._id = result.inserted_id
        return self._id

    def delete(self):
        if self._id:
            db = current_app.db_mongo
            db.patients.delete_one({'_id': self._id})
