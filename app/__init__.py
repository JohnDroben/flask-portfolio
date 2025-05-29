from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

db = SQLAlchemy()

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)


    # Базовая конфигурация
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Инициализация менеджера логина
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'





    # Конфигурация для загрузки файлов
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB

    # Создаем папку для загрузок, если ее нет
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Инициализация расширений
    db.init_app(app)
    migrate = Migrate(app, db)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Указываем страницу входа

    # Импорт моделей после инициализации db
    from app import models

    # Инициализация после создания приложения
    with app.app_context():
        from app.models import User
        from datetime import datetime

        # Обновление существующих пользователей
        users_without_date = User.query.filter(User.created_at == None).all()
        for user in users_without_date:
            user.created_at = datetime.utcnow()

        if users_without_date:
            db.session.commit()
            app.logger.info(f"Updated {len(users_without_date)} users with creation date")

    return app



    # Регистрация Blueprints
    from app.routes import main_bp, auth_bp, profile_bp, blog_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(blog_bp)

    return app



def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']