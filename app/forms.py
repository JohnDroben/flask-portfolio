from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User
from flask_login import current_user





class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя',
                          validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Повторите пароль',
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя пользователя уже занято')

def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email уже используется')



class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')



class ProfileForm(FlaskForm):
    username = StringField('Имя пользователя',
                          validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    current_password = PasswordField('Текущий пароль')
    new_password = PasswordField('Новый пароль', validators=[Length(min=6)])
    confirm_password = PasswordField('Подтвердите новый пароль')
    submit = SubmitField('Сохранить изменения')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Это имя пользователя уже занято')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Этот email уже используется')

    def validate_confirm_password(self, confirm_password):
        if self.new_password.data:
            if confirm_password.data != self.new_password.data:
                raise ValidationError('Пароли не совпадают')