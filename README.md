# Stroke Risk Assessment Application

A safe healthcare web app that will be used to treat patient records and stroke risk prediction. It is developed using Flask and SQLite as the authentication provider and MongoDB as the patient data provider and implements field-level encryption to ensure sensitive medical information is secure.

---

## What This Project Does

The application assists medical workers to handle patient data at the same time evaluate the risk of stroke on the basis of clinical data. The main goals are:

- Encrypt and control patient data.
- Offer rapid stroke risk evaluation on health measures.
- Ensure there is total audit trails to ensure compliance.
- Create secure and passwords controlled PDF reports.

The stroke causes death on a global scale. Early detection of at-risk patients is a life-saving practice, although medical data should be approached with a lot of security. The application is a solution to these two requirements.

---

## Core Features

**Patient Management**

Add, view, edit and delete patient records. Search patients by name and scroll through paginated searches (10 at a time). Input validation is found in all forms.

**Stroke Risk Prediction**

The algorithm checks on age, hypertension, heart disease, glucose levels, BMI, gender and smoking status. The findings indicate a percentage risk and classify the patients as low or high risk.

**Security**

The authentication of passwords is done using the hash algorithm of Argon2 which is memory-hard and resistant to attacks by the GPU. Two-factor authentication is based on TOTP and is compatible with Google Authenticator or Authy. Fernet (AES-128) is used to encrypt sensitive fields, such as glucose and BMI, and store them. The program has CSRF and rate limits as well as full audit trails.

**PDF Reports**

Export data on patients in the form of password-protected PDFs. The patient is the one whose password is his or her last name in lower case.

---

## Technical Architecture

The application has 2 databases:

SQLite manages user authentication - password hashes, email addresses, 2FA secrets, and usernames. It is quick with simple queries and good to the structured credential information.

MongoDB is used to store audit logs and patient records. The flexible schema is easy to add new patient fields to later on, and it also scales to the increased number of patients.

Patient sensitive information (glucose levels, BMI) is coded and saved in MongoDB. Attackers do not have the encryption key, therefore they cannot read the actual medical values even in case the database is compromised.

---

## Tech Stack

**Backend:** Flask 3.0, SQLAlchemy, PyMongo, Flask-Login, Flask-Talisman, Flask-Limiter.

**Frontend:** Flowbite, FontAwesome, Tailwind and Jinja2 templates.

**Security:** Argon2-CFFI, Cryptography (Fernet), PyOTP, Bleach.

**Reporting:** WeasyPrint, PyPDF, QRCode.

---

## Getting Started

### Prerequisites

You should have Python 3.8 and MongoDB installed in your system.

### Installation

Change Directory to the project directory:

```bash
cd /path/to/stroke-app
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

On Windows use `venv\Scripts\activate` instead.

Install dependencies:

```bash
pip install -r requirements.txt
```

Start MongoDB and run the application:

```bash
python run.py
```

Open http://127.0.0.1:5000 in your browser.

---

## Configuration

Create a `.env` file in the root directory:

```
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
MONGO_URI=mongodb://localhost:27018/stroke_app
ENCRYPTION_KEY=your-32-byte-base64-encoded-key
DATABASE_URL=sqlite:///app.db
```

To generate a new encryption key:

```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

---

## Running Tests

Run all tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app --cov-report=html
```

Run specific test files:

```bash
pytest tests/test_auth.py
pytest tests/test_patients.py
```

In the prject, user authentication, password hashing, 2FA, Security measures and patient CRUD operations are tested.

---

## Project Structure

```
stroke-app/
├── app/
│   ├── __init__.py          # Application factory
│   ├── extensions.py        # Flask extensions setup
│   ├── models/
│   │   ├── user.py          # User model (SQLite)
│   │   └── patient.py       # Patient model (MongoDB)
│   ├── auth/
│   │   ├── routes.py        # Login, register, 2FA routes
│   │   └── forms.py         # Authentication forms
│   ├── patients/
│   │   ├── routes.py        # Patient CRUD, prediction, export
│   │   └── forms.py         # Patient form
│   ├── api/
│   │   └── routes.py        # REST API endpoint
│   ├── home/
│   │   └── routes.py        # Homepage
│   ├── utils/
│   │   ├── crypto.py        # Encryption functions
│   │   ├── prediction.py    # Stroke risk algorithm
│   │   ├── pdf.py           # PDF generation
│   │   ├── audit.py         # Audit logging
│   │   └── charting.py      # Data visualization
│   ├── templates/           # Jinja2 HTML templates
│   └── static/              # CSS, JS, images
├── data/                    # MongoDB data directory
├── tests/
│   ├── conftest.py          # Test configuration
│   ├── test_auth.py         # Authentication tests
│   └── test_patients.py     # Patient tests
├── config.py                # App configuration
├── run.py                   # Entry point
├── requirements.txt         # Dependencies
└── README.md
```

---

## Troubleshooting

**Port 5000 already in use**

```bash
lsof -ti:5000 | xargs kill -9
```

**MongoDB connection failed**

Make sure MongoDB is running:

**Module not found errors**

Activate the virtual envronment and install dependencies from requirements.

```bash
source venv/bin/activate
pip install -r requirements.txt
```
