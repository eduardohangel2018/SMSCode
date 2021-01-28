#!/usr/bin/env python
import os
import click
from flask_migrate import Migrate, upgrade
from app import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

from app.models import User, Role, Permission, Topic, Comment


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission, Comment=Comment)


@app.cli.command()
@click.option('--length', default=25,
              help='Number of functions to include in the profile report')
@click.option('--profile-dir', default=None,
                help='Directory where profiler data files are saved')
def profile(length, profile_dir):
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length], profile_dir=profile_dir)


with app.app_context():
    db.create_all()
    port = int(os.environ.get("PORT", 9000))
    if __name__ == "__main__":
        app.run(port=port, debug=True)


@app.cli.command()
def deploy():
    upgrade()

    Role.insert_roles()
