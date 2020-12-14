import os
from flask_sqlalchemy import SQLAlchemy

DEBUG = True
SECRET_KEY = 'secret$'
TESTING = True
WTF_CSRF_ENABLED = False
# Connection and way to create database
SQLALCHEMY_DATABASE_URI = 'sqlite:///code-test.sqlite3'
SQLALCHEMY_TRACK_MODIFICATIONS = False