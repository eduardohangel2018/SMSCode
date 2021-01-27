from flask import Flask, Blueprint
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import config
from flask_pagedown import PageDown

# Extensions
bootstrap = Bootstrap()
db = SQLAlchemy()
lm = LoginManager()
lm.login_view = 'main.login'
moment = Moment()
pageDown = PageDown()


def create_app(config_name):
    print(config_name)
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config.DevelopmentConfig)

    bootstrap.init_app(app)
    db.init_app(app)
    lm.init_app(app)
    moment.init_app(app)
    pageDown.init_app(app)

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app


