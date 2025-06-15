from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.extensions import db, bcrypt
from app.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from app.utils import send_reset_email

# Define the auth blueprint for authentication-related routes
auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Log the user registration attempt
        print("Registering user:", form.username.data, form.email.data)

        # Hash the password before storing
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Create a new user instance and add to the database
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('auth.login'))
    else:
        # Show validation errors if form submission failed
        print("Register form errors:", form.errors)

    # Render registration page
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        # Find user by email
        user = User.query.filter_by(email=form.email.data).first()

        # Check password and login
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Logged in as {user.username}', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login failed. Check email and password.', 'danger')
            print("Login failed: incorrect email or password.")
    else:
        # Log any form validation issues
        print("Login form errors:", form.errors)

    # Render login page
    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    # Logout the user and redirect to home
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    # Prevent access to password reset if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RequestResetForm()
    if form.validate_on_submit():
        # Send password reset email
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions.', 'info')
        return redirect(url_for('auth.login'))

    # Render reset request form
    return render_template('reset_request.html', form=form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    from app.utils import verify_reset_token
    user = verify_reset_token(token)

    # If token is invalid or expired
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Update user's password with hashed new one
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('auth.login'))

    # Render new password form
    return render_template('reset_token.html', form=form)
