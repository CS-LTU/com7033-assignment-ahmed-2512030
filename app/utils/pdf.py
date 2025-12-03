from flask import make_response, render_template, flash, redirect, url_for
import io
from app.models.patient import Patient

try:
    from weasyprint import HTML
    from pypdf import PdfReader, PdfWriter
    import pydyf
    
    # Monkey patch pydyf.PDF to accept arguments
    # WeasyPrint 60.2 passes version and identifier, but pydyf 0.11.0 PDF.__init__ takes no args
    original_init = pydyf.PDF.__init__
    def patched_init(self, version=None, identifier=None, *args, **kwargs):
        original_init(self)
        if isinstance(version, str):
            version = version.encode('ascii')
        self.version = version or b'1.7'
        self.identifier = identifier
    pydyf.PDF.__init__ = patched_init
    
    HAS_PDF_LIBS = True
except ImportError:
    HAS_PDF_LIBS = False

def generate_encrypted_pdf(patient_id):
    patient = Patient.get_by_id(patient_id)
    if not patient:
        return None
        
    if not HAS_PDF_LIBS:
        raise Exception("PDF libraries not installed")

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
