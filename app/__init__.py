from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config


# Extensions
bootstrap = Bootstrap()
db = SQLAlchemy()
lm = LoginManager()
lm.login_view = 'main.login'
moment = Moment()


def create_app(config_name):
    # Application Instance
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize Extensions
    bootstrap.init_app(app)
    db.init_app(app)
    lm.init_app(app)
    moment.init_app(app)

    # Blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Flask-WTF
    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif']

    return app


