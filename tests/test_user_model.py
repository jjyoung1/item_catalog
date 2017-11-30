import unittest
from app import create_app, db
from app.models import User


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

    def test_password_setter(self):
        u = User(password='foo')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='foo')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='foo')
        self.assertTrue(u.verify_password('foo'))
        self.assertFalse(u.verify_password('bar'))

    def test_password_salts_are_random(self):
        u = User(password='foo')
        u2 = User(password='foo')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_user_create(self):
        u_id = User.create(email="john.doe@user.com",
                        username="John Doe",
                        password="foo")
        self.assertIsNotNone(u_id,'User creation failed')

        # Get User info
        user = User.getInfo(u_id)
        self.assertIsNotNone(user, 'User.getInfo failed to return User')
        # user.delete()

    def test_user_create_no_password(self):
        u_id = User.create(email="john.doe@user.com",
                           username="John Doe")
        self.assertIsNotNone(u_id, 'User creation failed')

        # Get User info
        user = User.getInfo(u_id)
        self.assertIsNotNone(user, 'User.getInfo() failed to return User')
        self.assertEqual(user.password_hash,'#', 'Password hash not set to #')
        # user.delete()

    def test_user_create_delete(self):
        u_id = User.create(email="john.doe@user.com",
                           username="John Doe")
        user = User.getInfo(u_id)
        user.delete()
