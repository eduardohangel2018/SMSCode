import imghdr
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from app.models import User
from datetime import datetime
from flask_moment import Moment


class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(1, 16)])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar Login')
    submit = SubmitField('Entrar')


class NameForm(FlaskForm):
    name = StringField('Digite seu nome:', validators=[DataRequired(), Length(1, 16)])
    submit = SubmitField('Enviar')


class RegistrationForm(FlaskForm):
    name = StringField('Nome Completo', validators=[DataRequired()])
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired(), EqualTo('password2',
                                                                          message='As senhas não conferem')])
    password2 = PasswordField('Digite Novamente', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Usuário já foi utilizado')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Senha Antiga', validators=[DataRequired()])
    password = PasswordField('Nova senha', validators=[DataRequired(), EqualTo('password2',
                                                                               message='As senhas não conferem')])
    password2 = PasswordField('Confirme sua Senha', validators=[DataRequired()])
    submit = SubmitField('Atualizar Senha')


class UploadForm(FlaskForm):
    text = StringField('Escreva seu Tópico:', validators=[DataRequired(), Length(1, 300)])
    image_file = FileField('Arquivo de Imagem')
    submit = SubmitField('Enviar')

    def validate_image_file(self, field):
        if field.data.filename[-4:].lower() != '.jpeg':
            raise ValidationError('Extensão inválida')
        if imghdr.what(field.data) != '.jpeg':
            raise ValidationError('Formato inválido')
