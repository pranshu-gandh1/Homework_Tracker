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
    app.config.from_object(Config)

    # Core app configuration
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # Flask-Login settings
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from app.routes.auth_routes import auth
    from app.routes.main_routes import main
    from app.routes.homework_routes import homework_bp
    from app.routes.extracurricular_routes import extracurricular_bp

    app.register_blueprint(combined_bp)
    app.register_blueprint(list_views)
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(homework_bp)
    app.register_blueprint(extracurricular_bp)
    
    return app
