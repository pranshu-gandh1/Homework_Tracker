from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import db
from app.models import Homework
from app.forms import HomeworkForm

homework_bp = Blueprint('homework_bp', __name__)  # Blueprint for homework routes

@homework_bp.route('/homework', methods=['GET'])
@login_required
def homework_list(): # List all homework assignments for the current user
    # Show homework assignments for current user
    homeworks = Homework.query.filter_by(user_id=current_user.id).order_by(Homework.due_date).all()
    return render_template('homework.html', homeworks=homeworks)

@homework_bp.route('/homework/add', methods=['GET', 'POST']) 
@login_required
def add_homework(): # Add a new homework item
    form = HomeworkForm()
    homeworks = Homework.query.filter_by(user_id=current_user.id).order_by(Homework.due_date).all()
    if form.validate_on_submit():
        hw = Homework(
            title=form.title.data,
            category=form.category.data,
            due_date=form.due_date.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(hw)
        db.session.commit()
        flash('Homework added!', 'success')
        return redirect(url_for('homework_bp.add_homework'))
    return render_template('add_homework.html', form=form, homeworks=homeworks)

@homework_bp.route('/homework/edit/<int:hw_id>', methods=['GET', 'POST'])
@login_required
def edit_homework(hw_id): # Edit an existing homework item
    # Edit a homework item
    hw = Homework.query.get_or_404(hw_id)
    if hw.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('homework_bp.homework_list'))
    form = HomeworkForm(obj=hw)
    if form.validate_on_submit():
        hw.title = form.title.data # Update title
        hw.category = form.category.data # Update category
        hw.due_date = form.due_date.data
        hw.description = form.description.data
        db.session.commit()
        flash('Homework updated!', 'success')
        return redirect(url_for('homework_bp.homework_list'))
    return render_template('edit_homework.html', form=form)

@homework_bp.route('/homework/delete/<int:hw_id>', methods=['POST'])
@login_required
def delete_homework(hw_id): # Delete a homework item
    # Delete a homework item
    hw = Homework.query.get_or_404(hw_id)
    if hw.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('homework_bp.homework_list'))
    db.session.delete(hw)
    db.session.commit()
    flash('Homework deleted.', 'info')
    return redirect(url_for('homework_bp.homework_list'))
