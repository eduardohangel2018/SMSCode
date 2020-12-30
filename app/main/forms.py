#!-*- conding: utf8 -*-
import imghdr
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from flask_wtf.file import FileField
from app.models import User, Role
from datetime import datetime
from flask_moment import Moment
from flask_pagedown.fields import PageDownField


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


class EditProfileForm(FlaskForm):
    name = StringField('Nome e Sobrenome', validators=[Length(0, 64)])
    location = StringField('Localização', validators=[Length(0, 64)])
    about_me = TextAreaField('Sobre mim')
    submit = SubmitField('Submit')


class EditProfileFormAdmin(FlaskForm):
    name = StringField('Nome Completo', validators=[Length(0, 64)])
    username = StringField('Usuário', validators=[Length(0, 64)])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Perfil', coerce=int)
    location = StringField('Localização', validators=[Length(0, 64)])
    about_me = TextAreaField('Sobre mim')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileFormAdmin, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Usuário já foi utilizado')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Senha Antiga', validators=[DataRequired()])
    password = PasswordField('Nova senha', validators=[DataRequired(), EqualTo('password2',
                                                                               message='As senhas não conferem')])
    password2 = PasswordField('Confirme sua Senha', validators=[DataRequired()])
    submit = SubmitField('Atualizar Senha')


class TopicForm(FlaskForm):
    body = PageDownField('Escreva o seu Tópico:', validators=[DataRequired()])
    submit = SubmitField('Salvar')
