from main import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), index=True, unique=True)
    name = db.Column(db.String(90))
    email = db.Column(db.String(90))
    password_hash = db.Column(db.String(128))
    topic = db.relationship('Topic', backref='topic')

    def __init__(self, username, name, email, password_hash):
        self.username = username
        self.name = name
        self.email = email
        self.password_hash = password_hash


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(199))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, text):
        self.text = text