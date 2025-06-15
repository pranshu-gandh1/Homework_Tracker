# Forms used in the app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask_login import current_user

# Registration form with validation
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()]) # Ensure username is provided
    email = StringField('Email', validators=[DataRequired(), Email()]) # Ensure email is valid
    password = PasswordField('Password', validators=[DataRequired()]) # Ensure password is provided
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) # Ensure password confirmation matches
    submit = SubmitField('Register') # Submit button for registration

    # Check for existing email
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')

    # Check for existing username
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() # Check if username already exists
        if user:
            raise ValidationError('Username already taken.')

# Login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()]) # Ensure email is valid
    password = PasswordField('Password', validators=[DataRequired()]) # Ensure password is provided
    remember = BooleanField('Remember Me') # Option to remember user
    submit = SubmitField('Login')

# Homework form
class HomeworkForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()]) # Title of homework
    category = StringField('Category', validators=[DataRequired()]) # Category of homework
    due_date = DateField('Due Date', validators=[DataRequired()]) # Due date for homework
    description = TextAreaField('Description') # Description of homework
    submit = SubmitField('Add Homework') # Submit button for homework form

# Extracurricular form
class ExtracurricularForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Add Extra Curricular')

# Password reset request form
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()]) # Ensure email is valid
    submit = SubmitField('Request Password Reset') # Submit button for password reset request

    # Validate if email exists
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No account with that email.') # Raise error if email not found

# Password reset form
class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()]) # Ensure new password is provided
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) # Ensure password confirmation matches
    submit = SubmitField('Reset Password')
