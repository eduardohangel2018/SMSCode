import imghdr
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError


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