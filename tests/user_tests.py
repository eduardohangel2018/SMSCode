import unittest
from app import create_app, db
from app.models import User


class UserModelTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        db.create_all()

    def tearDown(self):
        # Destroy all the databases table
        db.drop_all()
        # i pop the context
        self.app_ctx.pop()

    def test_password(self):
        u = User(username='eduardo')
        u.set_password('123456')
        self.assertTrue(u.verify_password('123456'))
        self.assertFalse(u.verify_password('654321'))

    def test_registration(self):
        User.register('eduardo', 'teste123')
        u = User.query.filter_by(username='eduardo').first()
        self.assertIsNotNone(u)
        self.assertTrue(u.verify_password('123456'))
        self.assertFalse(u.verify_password('654321'))
