from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Homework, Extracurricular

combined_bp = Blueprint('combined', __name__)  # Blueprint for combined assignments view

@combined_bp.route('/all_assignments')
@login_required
def all_assignments():
    # Get all homework and extracurriculars for the current user
    homeworks = Homework.query.filter_by(user_id=current_user.id).order_by(Homework.due_date.asc()).all()
    extracurriculars = Extracurricular.query.filter_by(user_id=current_user.id).order_by(Extracurricular.due_date.asc()).all()
    return render_template('all_assignments.html', homeworks=homeworks, extracurriculars=extracurriculars)
