# Helper functions for sending reset emails
from flask import url_for, current_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer as Serializer
from threading import Thread
from app.extensions import mail
from app.models import User  # Import your User model here

# Send email asynchronously
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

# Send password reset email with token
def send_reset_email(user):
    token = get_reset_token(user)
    msg = Message(
        subject='Password Reset Request',
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user.email]
    )
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email.
'''
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

# Generate reset token
def get_reset_token(user, expires_sec=1800):
    s = Serializer(current_app.config['SECRET_KEY'])
    return s.dumps({'user_id': user.id})

# Verify reset token and return user
def verify_reset_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token, max_age=1800)['user_id']
    except Exception:
        return None
    return User.query.get(user_id)
