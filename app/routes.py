from flask import render_template, redirect, url_for, request, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.forms import LoginForm, RegistrationForm, ProfileForm, PostForm
from app.models import User, Post

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
profile_bp = Blueprint('profile', __name__, url_prefix='/profile')
blog_bp = Blueprint('blog', __name__, url_prefix='/blog')

@main_bp.route('/')
def home():
    return render_template('home.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    # ... реализация логина ...

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    # ... реализация регистрации ...

@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    # ... реализация редактирования профиля ...

@blog_bp.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
    form = PostForm()
    # ... реализация блога ...