from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
csrf = CSRFProtect()


def create_app(config_name='default'):
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.routes import auth, main, calendar, messages
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(calendar.bp)
    app.register_blueprint(messages.bp)

    with app.app_context():
        db.create_all()

    return app

