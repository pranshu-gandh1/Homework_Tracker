from flask import Flask
from flask_migrate import Migrate
from config import Config
from app.extensions import db, bcrypt, login_manager, mail
from app.routes.homework_routes import homework_bp
from app.routes.dashboard_routes import dashboard_bp

migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Add these 2 lines for Flask-Login config:
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    mail.init_app(app)
    migrate.init_app(app, db)

    from app.routes.auth_routes import auth
    from app.routes.main_routes import main
    from app.routes.homework_routes import homework_bp
    from app.routes.extracurricular_routes import extracurricular_bp
    from app.routes.dashboard_routes import dashboard_bp

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(homework_bp)
    app.register_blueprint(extracurricular_bp)
    app.register_blueprint(dashboard_bp)
    
    return app
