import imghdr
import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# Conexão e Apontamento do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///code.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
# Inicializa a variavel global e instancia LoginManager
lm = LoginManager(app)
lm.login_view = 'login'


class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(1, 16)])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar Login')
    submit = SubmitField('Entrar')


class NameForm(FlaskForm):
    name = StringField('Digite seu nome:', validators=[DataRequired(), Length(1, 16)])
    submit = SubmitField('Enviar')


class UploadForm(FlaskForm):
    text = StringField('Escreva seu Tópico:', validators=[DataRequired(), Length(1, 300)])
    image_file = FileField('Arquivo de Imagem')
    submit = SubmitField('Enviar')

    def validate_image_file(self, field):
        if field.data.filename[-4:].lower() != '.jpeg':
            raise ValidationError('Extensão inválida')
        if imghdr.what(field.data) != '.jpeg':
            raise ValidationError('Formato inválido')


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), unique=True)
    name = db.Column(db.String(32))
    email = db.Column(db.String(32))
    password_hash = db.Column(db.String(64))

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

    # def __repr__(self):
    #     return '<User {0}>'.format(self.username)


# Flask-Login grava o estado do usuário através do user_id
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _text = db.Column(db.String(199))

    def __init__(self, id, _text):
        self.id = id
        self._text = _text


class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    _metadata = db.Column(db.String(199))

    def __init__(self, id, name, _metadata):
        self.id = id
        self.name = name
        self._metadata = _metadata


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/topic', methods=['GET', 'POST'])
def topic():
    image = None
    text = None
    form = UploadForm()
    if form.validate_on_submit():
        image = 'uploads/' + form.image_file.data.filename
        # app.static_folder é o path que o flask olha para onde irá renderizar as imagens na aplicação
        form.image_file.data.save(os.path.join(app.static_folder, image))
        text = form.text.data
    return render_template('topic.html', form=form, image=image, text=text)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Passa o nome que foi recebido no form
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        # Verifica se o password irá retornar falso
        if user is None or not user.verify_password(form.password.data):
            return redirect(url_for('login', **request.args))
        login_user(user, form.remember_me.data)
        # Tenho duas opções:
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html')


@app.route('/protected')
@login_required
def protected():
    return render_template('protected.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


# @app.before_first_request
# def create_database():
#     db.create_all()


# Se for chamado do main.py vai passar
if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
