from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Homework, Extracurricular

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    user_id = current_user.id
    homeworks = Homework.query.filter_by(user_id=user_id).order_by(Homework.due_date).all()
    extracurriculars = Extracurricular.query.filter_by(user_id=user_id).order_by(Extracurricular.due_date).all()
    return render_template('dashboard.html', homeworks=homeworks, extracurriculars=extracurriculars)
