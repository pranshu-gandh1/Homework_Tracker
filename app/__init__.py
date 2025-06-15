# App factory function for creating and configuring Flask app
from flask import Flask
from flask_migrate import Migrate
from config import Config
from app.extensions import db, bcrypt, login_manager, mail 
from app.routes.homework_routes import homework_bp
from app.routes.list_views_routes import list_views
from app.routes.combined_routes import combined_bp

migrate = Migrate()

def create_app(config_class=Config): 
    app = Flask(__name__)
    app.config.from_object(Config) # Load configuration from Config class

    # Core app configuration
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # Example database URI, change as needed

    # Initialize extensions
    db.init_app(app) # Initialize SQLAlchemy
    bcrypt.init_app(app) # Initialize Bcrypt for password hashing
    login_manager.init_app(app) # Initialize Flask-Login
    mail.init_app(app) # Initialize Flask-Mail for email handling
    migrate.init_app(app, db) # Initialize Flask-Migrate for database migrations

    # Flask-Login settings
    login_manager.login_view = 'auth.login' # Redirect to login page if not authenticated
    login_manager.login_message_category = 'info' # Category for login messages

    # Register blueprints
    from app.routes.auth_routes import auth # Authentication routes
    from app.routes.main_routes import main # Main application routes
    from app.routes.homework_routes import homework_bp # Homework management routes
    from app.routes.extracurricular_routes import extracurricular_bp # Extracurricular activities routes

    app.register_blueprint(combined_bp) # Combined routes for list views
    app.register_blueprint(list_views) # List views for homework and extracurriculars
    app.register_blueprint(auth) # Authentication routes
    app.register_blueprint(main) # Main application routes 
    app.register_blueprint(homework_bp) # Homework management routes
    app.register_blueprint(extracurricular_bp) # Extracurricular activities routes
    
    return app 
