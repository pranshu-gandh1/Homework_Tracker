# Blueprint for listing homework and extracurricular items
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Homework, Extracurricular

list_views = Blueprint('list_views', __name__)

@list_views.route('/homework')
@login_required  # Ensures only logged-in users can access this route
def homework_list():
    # Query homework items for the current user, ordered by due date
    homework_items = Homework.query.filter_by(user_id=current_user.id).order_by(Homework.due_date).all()
    return render_template('homework_list.html', homework_items=homework_items)

@list_views.route('/extracurricular')
@login_required
def extracurricular_list():
    # Query extracurricular items for the current user, ordered by due date
    extracurricular_items = Extracurricular.query.filter_by(user_id=current_user.id).order_by(Extracurricular.due_date).all()
    return render_template('extracurricular_list.html', extracurricular_items=extracurricular_items)
