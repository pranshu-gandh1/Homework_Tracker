# Database models and user loader
from datetime import datetime
from app.extensions import db, login_manager  
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from app import db

# Load user by ID for session management
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # Unique identifier for user
    username = db.Column(db.String(20), unique=True, nullable=False) # Username for the user
    email = db.Column(db.String(120), unique=True, nullable=False) # Email address for the user
    password = db.Column(db.String(60), nullable=False) # Password hash for the user
    homeworks = db.relationship('Homework', backref='owner', lazy=True) # Relationship to link homework to user
    extracurriculars = db.relationship('Extracurricular', backref='owner', lazy=True) # Relationship to link extracurriculars to user

    # Generate reset token
    def get_reset_token(self, expires_sec=1800): # Generate a token for password reset
        s = Serializer(current_app.config['SECRET_KEY']) 
        return s.dumps({'user_id': self.id})

    # Verify reset token
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

# Homework model
class Homework(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Unique identifier for homework
    title = db.Column(db.String(100), nullable=False) # Title of the homework
    category = db.Column(db.String(30), nullable=False) # Category of the homework
    due_date = db.Column(db.Date, nullable=False) # Due date for the homework
    description = db.Column(db.Text) # Description of the homework
    timestamp = db.Column(db.DateTime, default=datetime.utcnow) # Timestamp for when the homework was created
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Foreign key to link homework to a user

# Extracurricular model
class Extracurricular(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    category = db.Column(db.String(140), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
