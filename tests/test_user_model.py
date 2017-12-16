import unittest
from app import create_app, db
from app.models.user import User
from flask import jsonify


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_create(self):
        u_id = User.create(email="john.doe@user.com",
                           username="John Doe",
                           password="foo")
        self.assertIsNotNone(u_id, 'User creation failed')

        # Get User info
        user = User.getInfo(u_id)
        self.assertIsNotNone(user, 'User.getInfo failed to return User')
        # user.delete()

    def test_user_create_delete(self):
        u_id = User.create(email="john.doe@user.com",
                           username="John Doe")
        user = User.getInfo(u_id)
        user.delete()
