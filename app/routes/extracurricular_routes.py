from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import db
from app.models import Extracurricular
from app.forms import ExtracurricularForm

extracurricular_bp = Blueprint('extracurricular_bp', __name__)  # Blueprint for extracurricular routes

@extracurricular_bp.route('/extracurricular', methods=['GET'])
@login_required
def extracurricular_list():
    # Show extracurricular activities for current user
    extracurriculars = Extracurricular.query.filter_by(user_id=current_user.id).order_by(Extracurricular.due_date).all()
    return render_template('extracurricular.html', extracurriculars=extracurriculars)

@extracurricular_bp.route('/extracurricular/add', methods=['GET', 'POST'])
@login_required
def add_extracurricular():
    #Add an extracurricular activity
    form = ExtracurricularForm()
    extracurriculars = Extracurricular.query.filter_by(user_id=current_user.id).order_by(Extracurricular.due_date).all()
    if form.validate_on_submit():
        ec = Extracurricular(
            title=form.title.data,
            category=form.category.data,
            due_date=form.due_date.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(ec) # Add new extracurricular to the database
        db.session.commit() # Commit changes to the database
        flash('Extra Curricular added!', 'success')
        return redirect(url_for('extracurricular_bp.add_extracurricular')) # Redirect to the add extracurricular page to show updated list
    return render_template('add_extracurricular.html', form=form, extracurriculars=extracurriculars) # Render the add extracurricular form with existing extracurriculars

@extracurricular_bp.route('/extracurricular/edit/<int:ec_id>', methods=['GET', 'POST'])
@login_required
def edit_extracurricular(ec_id):
    # Edit an existing extracurricular by id
    user_id=current_user.id
    ec = Extracurricular.query.get_or_404(ec_id)
    if ec.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('extracurricular_bp.extracurricular_list'))
    form = ExtracurricularForm(obj=ec)
    if form.validate_on_submit():
        ec.title = form.title.data # Update title
        ec.category = form.category.data # Update category
        ec.due_date = form.due_date.data # Update due date
        ec.description = form.description.data # Update description
        db.session.commit() # Commit changes to the database
        flash('Extra Curricular updated!', 'success')
        return redirect(url_for('extracurricular_bp.extracurricular_list'))
    return render_template('edit_extracurricular.html', form=form)

@extracurricular_bp.route('/extracurricular/delete/<int:ec_id>', methods=['POST']) # Delete an extracurricular activity
@login_required
def delete_extracurricular(ec_id):
    # Delete extracurricular if user owns it
    ec = Extracurricular.query.get_or_404(ec_id)
    if ec.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('extracurricular_bp.extracurricular_list'))
    db.session.delete(ec)
    db.session.commit()
    flash('Extra Curricular deleted.', 'info')
    return redirect(url_for('extracurricular_bp.extracurricular_list'))
