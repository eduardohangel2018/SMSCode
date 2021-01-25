from functools import wraps
from flask_httpauth import HTTPBasicAuth
from flask import g
from sqlalchemy.sql.functions import user
from werkzeug.exceptions import abort
from .errors import forbidden
from app.models import Permission
from flask_login import current_user


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                return forbidden('Permissao Insuficiente')
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# def api_auth(username, password):
#     def decorator(f):
#         @wraps(f)
#         def decorated_func(*args, **kwargs):
#             if username == '':
#                 g.current_user = AnonymousUser()
#                 return True
#             if not user:
#                 return False
#             g.current_user = user
#             return f(*args, **kwargs)
#         return user.verify_password(password)
#     return decorator


# def api_auth(permission):
#     def decorator(fn):
#         def wrapper(*args):
#             if username == '':
#                 return True
#                 return fn(*args)
#         return wrapper
#     return decorator
