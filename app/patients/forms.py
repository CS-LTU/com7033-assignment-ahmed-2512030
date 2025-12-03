from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, InputRequired

class PatientForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[InputRequired(), NumberRange(min=0, max=120)])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    hypertension = SelectField('Hypertension', choices=[(0, 'No'), (1, 'Yes')], coerce=int, validators=[InputRequired()])
    heart_disease = SelectField('Heart Disease', choices=[(0, 'No'), (1, 'Yes')], coerce=int, validators=[InputRequired()])
    avg_glucose_level = FloatField('Avg Glucose Level', validators=[InputRequired(), NumberRange(min=50, max=500, message="Glucose level must be between 50-500 mg/dL")])
    bmi = FloatField('BMI', validators=[InputRequired(), NumberRange(min=10, max=100, message="BMI must be between 10-100")])
    smoking_status = SelectField('Smoking Status', choices=[
        ('formerly smoked', 'Formerly Smoked'),
        ('never smoked', 'Never Smoked'),
        ('smokes', 'Smokes'),
        ('Unknown', 'Unknown')
    ], validators=[DataRequired()])
    work_type = SelectField('Work Type', choices=[
        ('Private', 'Private'),
        ('Self-employed', 'Self-employed'),
        ('Govt_job', 'Govt Job'),
        ('children', 'Children'),
        ('Never_worked', 'Never Worked')
    ], validators=[DataRequired()])
    residence_type = SelectField('Residence Type', choices=[('Urban', 'Urban'), ('Rural', 'Rural')], validators=[DataRequired()])
    submit = SubmitField('Save Patient')
