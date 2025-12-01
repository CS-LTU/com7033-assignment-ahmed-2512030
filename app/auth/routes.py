from flask import render_template, redirect, url_for, flash, request, session, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.auth.forms import LoginForm, RegistrationForm, TwoFactorForm
from app.models.user import User
import pyotp
import qrcode
import io
import base64

auth = Blueprint('auth', __name__)

from app.utils.audit import log_audit

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('patients.index')) # Redirect to main dashboard
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            # If 2FA is enabled, redirect to 2FA verification
            if user.is_2fa_enabled:
                session['2fa_user_id'] = user.id
                return redirect(url_for('auth.verify_2fa'))
            
            login_user(user, remember=form.remember_me.data)
            log_audit('login', {'username': user.username})
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('patients.index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            # Note: Cannot log user ID here as not authenticated, but could log failed attempt with username
    return render_template('auth/login.html', title='Login', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('patients.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        # Generate a random secret for 2FA (initially disabled)
        user.totp_secret = pyotp.random_base32()
        db.session.add(user)
        db.session.commit()
        log_audit('register', {'username': user.username})
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@auth.route('/logout')
def logout():
    log_audit('logout')
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/verify-2fa', methods=['GET', 'POST'])
def verify_2fa():
    if '2fa_user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['2fa_user_id'])
    if not user:
        return redirect(url_for('auth.login'))

    form = TwoFactorForm()
    if form.validate_on_submit():
        totp = pyotp.TOTP(user.totp_secret)
        if totp.verify(form.otp.data):
            login_user(user)
            session.pop('2fa_user_id', None)
            log_audit('login_2fa', {'username': user.username})
            return redirect(url_for('patients.index'))
        else:
            flash('Invalid OTP', 'danger')
            
    return render_template('auth/verify_2fa.html', title='Two-Factor Authentication', form=form)

@auth.route('/setup-2fa', methods=['GET', 'POST'])
@login_required
def setup_2fa():
    if current_user.is_2fa_enabled:
        flash('2FA is already enabled.', 'info')
        return redirect(url_for('patients.index'))

    # Generate QR Code
    totp = pyotp.TOTP(current_user.totp_secret)
    uri = totp.provisioning_uri(name=current_user.email, issuer_name="StrokeApp")
    
    img = qrcode.make(uri)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    form = TwoFactorForm()
    if form.validate_on_submit():
        if totp.verify(form.otp.data):
            current_user.is_2fa_enabled = True
            db.session.commit()
            flash('Two-Factor Authentication enabled!', 'success')
            return redirect(url_for('patients.index'))
        else:
            flash('Invalid OTP', 'danger')

    return render_template('auth/setup_2fa.html', title='Setup 2FA', form=form, qr_code=img_str, secret=current_user.totp_secret)
