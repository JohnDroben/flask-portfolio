from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from sqlalchemy import inspect

# Инициализация расширений
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # Базовая конфигурация
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB

    # Создание папки для загрузок
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Инициализация расширений с приложением
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Указываем страницу входа

    # Регистрация Blueprints
    from app.routes import main_bp, auth_bp, profile_bp, blog_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(blog_bp)


    # Инициализация базы данных и проверка структуры
    with app.app_context():
        # Создаем таблицы, если их нет
        db.create_all()

        # Проверяем наличие поля created_at в таблице user
        from app.models import User
        inspector = inspect(db.engine)

        # Проверяем, существует ли таблица user
        if 'user' in inspector.get_table_names():
            columns = [col['name'] for col in inspector.get_columns('user')]

            # Добавляем поле created_at, если оно отсутствует
            if 'created_at' not in columns:
                try:
                    with db.engine.connect() as conn:
                        conn.execute('ALTER TABLE user ADD COLUMN created_at DATETIME')
                        conn.execute('UPDATE user SET created_at = CURRENT_TIMESTAMP')
                        print("Added 'created_at' column to user table")
                except Exception as e:
                    print(f"Error adding created_at column: {e}")

    return app