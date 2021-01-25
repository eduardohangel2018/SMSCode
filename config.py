#!-*- conding: utf8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = True
    SECRET_KEY = 'secret$'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    # Grava estatísticas de consulta, definindo o limite de consulta lenta para 0.5 segundos
    FLASK_SLOW_DB_QUERY_TIME = 0.5
    FLASK_ADMIN_USER = 'Flask Admin <ADMINISTRATOR>'
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN')
    FLASK_TOPICS_PER_PAGE = 10
    FLASK_COMMENTS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app/data-dev3.sqlite3')


class TestingConfig(Config):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': "config.DevelopmentConfig"
}
