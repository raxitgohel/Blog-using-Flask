from app import db, login_manager
from flask import current_app
from datetime import datetime
from flask_login import UserMixin
import jwt
from time import time

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_image = db.Column(db.String(20), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', back_populates='author', lazy=True)
    
    def get_reset_token(self, expires_sec=600):
        payload = {'user_id': self.id, 'exp': time() + expires_sec}
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        return token
        
    @staticmethod
    def verify_reset_token(token):
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = payload['user_id']
            return User.query.get(user_id)
        except jwt.ExpiredSignatureError:
            # Token has expired
            return None
        except jwt.InvalidTokenError:
            # Token is invalid
            return None

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.profile_image}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', back_populates='posts')

    def __repr__(self) -> str:
        return f"Post('{self.title}', '{self.date_posted}')"