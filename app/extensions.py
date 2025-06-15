# Extensions used across the app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()  # Database instance
bcrypt = Bcrypt()  # For password hashing
login_manager = LoginManager()  # Login manager
mail = Mail()  # Email manager
