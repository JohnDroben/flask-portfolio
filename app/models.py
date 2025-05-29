from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    profile_image = db.Column(db.String(200), default='default-avatar.jpg')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_id(self):
        return self.id

    def get_profile_image(self):
        return self.profile_image

    def set_profile_image(self, image):
        self.profile_image = image

        return self

    def get_email(self):
        return self.email

    def get_username(self):
        return self.username

    def set_username(self, username):
        self.username = username

        return self

    def set_email(self, email):
        self.email = email

        return self

    def get_created_at(self):
        if self.created_at:
            return self.created_at.strftime('%d.%m.%Y')
        return "Неизвестно"

    def set_created_at(self, created_at):
        self.created_at = created_at
        return self

    def get_password_hash(self):
        return self.password_hash

    def set_password_hash(self, password_hash):
        self.password_hash = password_hash
        return self



    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

