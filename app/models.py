from flask import Flask
from . import db, lm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), unique=True)
    name = db.Column(db.String(32))
    email = db.Column(db.String(32))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def register(username, password):
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    def __repr__(self):
        return '<User {0}>'.format(self.username)


@lm.user_loader
def load_user(_id):
    return User.query.get(int(_id))


class Comment(db.Model):
    __tablename__ = 'comments'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _text = db.Column(db.String(199))

    def __init__(self, _id, _text):
        self._id = _id
        self._text = _text


class Topic(db.Model):
    __tablename__ = 'topics'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    _metadata = db.Column(db.String(199))

    def __init__(self, _id, name, _metadata):
        self._id = _id
        self.name = name
        self._metadata = _metadata
