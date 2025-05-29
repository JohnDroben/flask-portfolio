from flask import render_template, Blueprint, redirect, url_for, flash, current_app, request
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from app import db, allowed_file
from app.models import User
from app.forms import LoginForm, RegistrationForm, ProfileForm
import os
from werkzeug.utils import secure_filename
from flask import app




# Главные маршруты
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    return render_template('home.html',
                           current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Маршруты аутентификации
auth_bp = Blueprint('auth', __name__)


@app.before_first_request
def update_existing_users():
    from app.models import User
    from datetime import datetime

    users_without_date = User.query.filter(User.created_at == None).all()
    for user in users_without_date:
        user.created_at = datetime.utcnow()

    if users_without_date:
        db.session.commit()
        print(f"Updated {len(users_without_date)} users with creation date")


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by (username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, created_at=datetime.utcnow())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


# Маршруты профиля
profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/edit', methods=['GET', 'POST'])

@profile_bp.route('/account')

@login_required
def account():
    return render_template('profile/account.html')


def edit():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        flash('Вы успешно вошли в систему!', 'success')

        if form.current_password.data and form.new_password.data:
            if current_user.check_password(form.current_password.data):
                current_user.set_password(form.new_password.data)
                flash('Пароль успешно изменен', 'success')

            else:
                flash('Неверный текущий пароль', 'danger')
                return redirect(url_for('profile.edit'))
        # Сохранение изменений
        db.session.commit()
        flash('Профиль успешно обновлен', 'success')
        return redirect(url_for('profile.account'))
    return render_template('profile/edit.html', form=form)


# Маршруты блога
blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/posts')
def posts():
    return render_template('blog/posts.html')


@profile_bp.route('/update', methods=['POST'])
@login_required
def update():
    form = ProfileForm()

    if form.validate_on_submit():
        # Обновление основных данных
        current_user.username = form.username.data
        current_user.email = form.email.data

        # Обновление пароля
        if form.current_password.data and form.new_password.data:
            if current_user.check_password(form.current_password.data):
                current_user.set_password(form.new_password.data)
                flash('Пароль успешно изменен', 'success')
            else:
                flash('Неверный текущий пароль', 'danger')
                return redirect(url_for('profile.account'))

        # Обновление аватара
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file.filename != '' and allowed_file(file.filename):
                # Генерируем уникальное имя файла
                filename = f"{current_user.id}_{secure_filename(file.filename)}"
                filepath = os.path.join(
                    current_app.config['UPLOAD_FOLDER'],
                    filename
                )
                file.save(filepath)
                current_user.profile_image = f"static/uploads/{filename}"
                flash('Аватар успешно обновлен', 'success')
            elif file.filename != '':
                flash('Недопустимый формат файла. Разрешены: PNG, JPG, JPEG, GIF', 'danger')

        # Сохранение изменений
        db.session.commit()
        flash('Профиль успешно обновлен', 'success')
        return redirect(url_for('profile.account'))

    # Если форма не прошла валидацию
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Ошибка в поле {getattr(form, field).label.text}: {error}', 'danger')

    return redirect(url_for('profile.account'))