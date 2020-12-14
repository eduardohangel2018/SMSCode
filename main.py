#!/usr/bin/env python
from app import create_app, db
from app.models import User

if __name__ == '__main__':
    app = create_app('dev')
    with app.app_context():
        db.create_all()
        if User.query.filter_by(username='eduardo').first() is None:
            User.register('eduardo', '123456')
        app.run()
