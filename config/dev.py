import os
from flask_sqlalchemy import SQLAlchemy

DEBUG = True
SECRET_KEY = 'secret$'
# Conexão e Apontamento do banco
SQLALCHEMY_DATABASE_URI = 'sqlite:///code.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = False
