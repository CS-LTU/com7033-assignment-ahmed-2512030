from flask import make_response, render_template, flash, redirect, url_for
from weasyprint import HTML
from pypdf import PdfReader, PdfWriter
import io
from app.models.patient import Patient

def generate_encrypted_pdf(patient_id):
    patient = Patient.get_by_id(patient_id)
    if not patient:
        return None

    # Render HTML for PDF
    html_content = render_template('patients/pdf_template.html', patient=patient)
    
    # Generate PDF
    pdf_bytes = HTML(string=html_content).write_pdf()
    
    # Encrypt PDF
    # Password is patient's last name (lowercase) for simplicity in this demo
    password = patient.last_name.lower()
    
    reader = PdfReader(io.BytesIO(pdf_bytes))
    writer = PdfWriter()
    
    for page in reader.pages:
        writer.add_page(page)
    
    writer.encrypt(password)
    
    output_stream = io.BytesIO()
    writer.write(output_stream)
    output_stream.seek(0)
    
    return output_stream, password
