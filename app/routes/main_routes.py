# Main routes for homepage, dashboard, and help page
from flask import Blueprint, render_template
from flask_login import login_required

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Home page
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    # Dashboard view (protected)
    return render_template('all_assignments.html')

@main.route('/help')
def help():
    # Help page
    return render_template('help.html')
