import imghdr
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, ValidationError, Required

from config import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

bootstrap = Bootstrap(app)
moment = Moment(app)

# Conexão e Apontamento do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///code.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class NameForm(FlaskForm):
    name = StringField('Digite seu nome:', validators=[DataRequired(), Length(1, 16)])
    submit = SubmitField('Enviar')


class UploadForm(Form):
    name = StringField('Escreva seu Tópico:', validators=[DataRequired(), Length(1, 128)])
    image_file = FileField('Arquivo de Imagem')
    submit = SubmitField('Enviar')

    def validate_image_file(self, field):
        if field.data.filename[-4:].lower() != '.jpeg':
            raise ValidationError('Extensão inválida')
        if imghdr.what(field.data) != '.jpeg':
            raise ValidationError('Formato inválido')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


@app.route('/')
@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
    return render_template('index.html', current_time=datetime.utcnow(), name=name, form=form)


@app.route('/topic', methods=['GET', 'POST'])
def topic():
    image = None
    form = UploadForm()
    if form.validate_on_submit():
        image = 'uploads/' + form.image_file.data.filename
        # app.static_folder é o path que o flask olha para onde irá renderizar as imagens na aplicação
        form.image_file.data.save(os.path.join(app.static_folder, image))
    return render_template('topic.html', form=form, image=image)


@app.before_first_request
def create_database():
    db.create_all()


if __name__ == '__main__':
    from config import db
    db.init_app(app)
    app.run(debug=True)
