#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User


if __name__ == '__main__':
    app = create_app('dev')
    with app.app_context():
        db.create_all()
        # if User.query.filter_by(name='administrator', username='admin').first() is None:
        #     User.register('administrator', 'admin', '123456')
        app.run()
