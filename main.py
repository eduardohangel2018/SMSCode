#!/usr/bin/env python
import os
from flask_migrate import Migrate, upgrade
from app import create_app, db


if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    migrate = Migrate(app, db)

    from app.models import User, Role, Permission

    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User, Role=Role, Permission=Permission)

    @app.cli.command()
    def deploy():
        upgrade()
        Role.insert_roles()

    with app.app_context():
        db.create_all()
        app.run()
