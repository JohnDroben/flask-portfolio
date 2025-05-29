from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # Базовая конфигурация
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Инициализация расширений
    db.init_app(app)
    migrate = Migrate(app, db)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Указываем страницу входа

    # Импорт моделей после инициализации db
    from app import models

    # Регистрация Blueprints
    from app.routes import main_bp, auth_bp, profile_bp, blog_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(blog_bp)

    return app