import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

# Conexão e Apontamento do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///code.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


class NameForm(FlaskForm):
    name = StringField('Digite seu nome:', validators=[DataRequired()])
    submit = SubmitField('Enviar')


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


if __name__ == '__main__':
    app.run(debug=True)
