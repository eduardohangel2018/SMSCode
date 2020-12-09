from flask_sqlalchemy import SQLAlchemy
from config import db


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20))
    name = db.Column(db.String(90))
    email = db.Column(db.String(90))
    password_hash = db.Column(db.String(128))

    def __init__(self, user_id, username, name, email, password_hash):
        self.user_id = user_id
        self.username = username
        self.name = name
        self.email = email
        self.password_hash = password_hash


class Comment(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(199))

    def __init__(self, comment_id, text):
        self.comment_id = comment_id
        self.text = text


class Topic(db.Model):
    __tablename__ = 'topics'
    topic_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    metadata = db.Column(db.String(199))

    def __init__(self, topic_id, name, metadata):
        self.topic_id = topic_id
        self.name = name
        self.metadata = metadata


