import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from app.models.patient import Patient

def generate_stroke_stats_chart():
    patients = Patient.get_all(limit=1000) # Get a sample
    
    if not patients:
        return None

    # Data preparation
    genders = {'Male': 0, 'Female': 0, 'Other': 0}
    stroke_risks = {'High': 0, 'Low': 0}
    
    for p in patients:
        if p.gender in genders:
            genders[p.gender] += 1
        
        # Simple risk estimation for chart
        risk = 0
        if p.age > 60: risk += 1
        if p.hypertension == '1': risk += 1
        if p.heart_disease == '1': risk += 1
        
        if risk >= 2:
            stroke_risks['High'] += 1
        else:
            stroke_risks['Low'] += 1

    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    
    # Gender Pie Chart
    ax1.pie(genders.values(), labels=genders.keys(), autopct='%1.1f%%', startangle=90)
    ax1.set_title('Patient Gender Distribution')
    
    # Risk Bar Chart
    ax2.bar(stroke_risks.keys(), stroke_risks.values(), color=['red', 'green'])
    ax2.set_title('Estimated Stroke Risk Distribution')
    
    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    return base64.b64encode(buf.getvalue()).decode('utf-8')
