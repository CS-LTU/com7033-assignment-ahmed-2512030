from flask import Blueprint, render_template
from flask_login import login_required

home = Blueprint('home', __name__)

@home.route('/')
@home.route('/index')
@login_required
def index():
    return render_template('home/index.html', title='Dashboard')
