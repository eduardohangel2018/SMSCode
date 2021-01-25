#!-*- conding: utf8 -*-
from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from ..models import User, AnonymousUser
from .errors import unauthorized, forbidden
from . import api

authenticate = HTTPBasicAuth()


@authenticate.verify_password
def verify_password(username, password):
    if username == '':
        g.current_user = AnonymousUser()
        return True
    user = User.query.filter_by(username=username).first()
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)


@authenticate.error_handler
def auth_error():
    return unauthorized('Credenciais Invalidas')


@api.before_request
@authenticate.login_required()
def before_request():
    if not g.current_user.is_anonymous and not g.current_user.confirmed:
        return forbidden('Conta de usuario invalida')


@api.route('/tokens/', methods=['POST'])
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Credenciais Invalidas')
    return jsonify({'token': g.current_user.generate_auth_token})
