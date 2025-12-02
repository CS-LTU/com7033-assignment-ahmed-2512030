from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.patients.forms import PatientForm
from app.models.patient import Patient
from bson import ObjectId
from app.utils.audit import log_audit

patients = Blueprint('patients', __name__)

# root route for patients
@patients.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '')
    per_page = 10
    skip = (page - 1) * per_page
    
    #  parameterized queries
    patient_list = Patient.get_all(limit=per_page, skip=skip, search_query=search_query) 
    return render_template('patients/index.html', patients=patient_list, page=page, search_query=search_query)

@patients.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            age=form.age.data,
            gender=form.gender.data,
            hypertension=form.hypertension.data,
            heart_disease=form.heart_disease.data,
            avg_glucose_level=form.avg_glucose_level.data,
            bmi=form.bmi.data,
            smoking_status=form.smoking_status.data,
            work_type=form.work_type.data,
            residence_type=form.residence_type.data
        )
        patient_id = patient.save()
        log_audit('add_patient', {'patient_id': str(patient_id), 'name': f"{patient.first_name} {patient.last_name}"})
        flash('Patient added successfully!', 'success')
        return redirect(url_for('patients.index'))
    return render_template('patients/add.html', title='Add Patient', form=form)

@patients.route('/edit/<patient_id>', methods=['GET', 'POST'])
@login_required
def edit(patient_id):
    patient = Patient.get_by_id(patient_id)
    if not patient:
        flash('Patient not found', 'danger')
        return redirect(url_for('patients.index'))
    
    form = PatientForm()
    if request.method == 'GET':
        form.first_name.data = patient.first_name
        form.last_name.data = patient.last_name
        form.age.data = patient.age
        form.gender.data = patient.gender
        form.hypertension.data = patient.hypertension
        form.heart_disease.data = patient.heart_disease
        form.avg_glucose_level.data = float(patient.avg_glucose_level) if patient.avg_glucose_level else 0.0
        form.bmi.data = float(patient.bmi) if patient.bmi else 0.0
        form.smoking_status.data = patient.smoking_status
        form.work_type.data = patient.work_type
        form.residence_type.data = patient.residence_type

    if form.validate_on_submit():
        patient.first_name = form.first_name.data
        patient.last_name = form.last_name.data
        patient.age = form.age.data
        patient.gender = form.gender.data
        patient.hypertension = form.hypertension.data
        patient.heart_disease = form.heart_disease.data
        patient.avg_glucose_level = form.avg_glucose_level.data
        patient.bmi = form.bmi.data
        patient.smoking_status = form.smoking_status.data
        patient.work_type = form.work_type.data
        patient.residence_type = form.residence_type.data
        
        patient.save()
        log_audit('edit_patient', {'patient_id': str(patient_id)})
        flash('Patient updated successfully!', 'success')
        return redirect(url_for('patients.index'))
        
    return render_template('patients/edit.html', title='Edit Patient', form=form, patient_id=patient_id)

@patients.route('/delete/<patient_id>', methods=['POST'])
@login_required
def delete(patient_id):
    patient = Patient.get_by_id(patient_id)
    if patient:
        patient.delete()
        log_audit('delete_patient', {'patient_id': str(patient_id)})
        flash('Patient deleted successfully', 'success')
    else:
        flash('Patient not found', 'danger')
    return redirect(url_for('patients.index'))

@patients.route('/view/<patient_id>')
@login_required
def view(patient_id):
    patient = Patient.get_by_id(patient_id)
    if not patient:
        flash('Patient not found', 'danger')
        return redirect(url_for('patients.index'))
    log_audit('view_patient', {'patient_id': str(patient_id)})
    return render_template('patients/view.html', title='View Patient', patient=patient)

from app.utils.prediction import predict_stroke_risk
from app.utils.pdf import generate_encrypted_pdf
from flask import send_file

@patients.route('/predict/<patient_id>', methods=['POST'])
@login_required
def predict(patient_id):
    patient = Patient.get_by_id(patient_id)
    if not patient:
        flash('Patient not found', 'danger')
        return redirect(url_for('patients.index'))
    
    try:
        # Decrypt sensitive fields for prediction, in memory decryption used.
        prediction, probability = predict_stroke_risk(
            patient.age,
            patient.hypertension,
            patient.heart_disease,
            patient.avg_glucose_level,
            patient.bmi,
            patient.gender,
            patient.smoking_status
        )
        
        risk_percentage = round(probability * 100, 2)
        risk_level = "High" if risk_percentage > 50 else "Low"
        
        log_audit('predict_stroke', {'patient_id': str(patient_id), 'risk': risk_percentage})
        
        flash(f'Stroke Risk Prediction: {risk_level} Risk ({risk_percentage}%)', 'info')
    except Exception as e:
        flash(f'Prediction failed: {str(e)}', 'danger')
    
    return redirect(url_for('patients.view', patient_id=patient_id))

@patients.route('/export/<patient_id>')
@login_required
def export_pdf(patient_id):
    try:
        pdf_stream, password = generate_encrypted_pdf(patient_id)
        if not pdf_stream:
            flash('Patient not found', 'danger')
            return redirect(url_for('patients.index'))
            
        log_audit('export_pdf', {'patient_id': str(patient_id)})
        
        # Flash the password to the user (in a real app, this might be handled differently)
        flash(f'PDF exported successfully. Password is: {password}', 'success')
        
        return send_file(
            pdf_stream,
            as_attachment=True,
            download_name=f'patient_{patient_id}.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        flash(f'Export failed: {str(e)}', 'danger')
        return redirect(url_for('patients.view', patient_id=patient_id))
