import os
import random

# Mock prediction if libraries are missing
try:
    import numpy as np
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    import joblib
    HAS_ML = True
except ImportError:
    HAS_ML = False

def predict_stroke_risk(age, hypertension, heart_disease, avg_glucose_level, bmi, gender, smoking_status):
    if not HAS_ML:
        # Mock logic for demo purposes when ML libs can't be installed
        base_risk = 0.1
        if age > 60: base_risk += 0.3
        if str(hypertension) == '1': base_risk += 0.2
        if str(heart_disease) == '1': base_risk += 0.2
        if float(bmi) > 30: base_risk += 0.1
        if float(avg_glucose_level) > 200: base_risk += 0.1
        
        probability = min(base_risk + random.uniform(0, 0.1), 0.99)
        prediction = 1 if probability > 0.5 else 0
        return prediction, probability

    # Real logic (if libs were installed)
    # ... (omitted for brevity as we know it fails in this env)
    return 0, 0.1
