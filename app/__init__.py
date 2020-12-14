import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Extensions
bootstrap = Bootstrap()
db = SQLAlchemy()
lm = LoginManager()
lm.login_view = 'main.login'


def create_app(config_name):
    # Application Instance
    app = Flask(__name__)

    # Import Configuration
    cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
    app.config.from_pyfile(cfg)

    # Initialize Extensions
    bootstrap.init_app(app)
    db.init_app(app)
    lm.init_app(app)

    # Blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Configure production logging errors
    if not app.config['DEBUG'] and not app.config['TEST']:
        import logging
        from logging.handlers import SMTPHandler
        mail_handler = SMTPHandler('127.0.0.1', 'example@example.com',
                                   app.config['ADMINS'], 'Application Error')
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    return app


