import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = True
    SECRET_KEY = 'secret$'

    # Conexão e Apontamento do banco
    SQLALCHEMY_DATABASE_URI = 'sqlite:///teste-code.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN = 'FLASK_ADMIN'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

