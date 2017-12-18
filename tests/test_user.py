from unittest import TestCase
from app.models.user import User
from itsdangerous import BadSignature, SignatureExpired
import time

class TestUser(TestCase):
    username = 'myname'
    email = 'myname@myname.com'
    password = 'mypass'
    picture = 'photo_url'

    def setUp(self):
        print("Hello")

    def test_password(self):
        user = TestUser.createUser()
        self.assertTrue(user.password_hash is not None)
        with self.assertRaises(AttributeError):
            user.password
        # noinspection PyTypeChecker
        user = TestUser.createUser(password=None)
        self.assertEqual(user.password_hash, '#', 'Password hash not set to #')

    def test_verify_password(self):
        u = TestUser.createUser()
        self.assertTrue(u.verify_password(TestUser.password))
        self.assertFalse(u.verify_password('badpassword'))

    def test_password_salts_are_random(self):
        u = TestUser.createUser()
        u2 = TestUser.createUser()
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_serialize(self):
        user = TestUser.createUser()
        user.picture = TestUser.picture
        user.id = 1

        # Get User info
        s_user = user.serialize()
        self.assertEqual(s_user['id'], 1)
        self.assertEqual(s_user['username'], TestUser.username)
        self.assertEqual(s_user['email'], TestUser.email)
        self.assertEqual(s_user['picture'], TestUser.picture)

    def test_verify_auth_token(self):
        user = TestUser.createUser()
        user.id = 1

        # Create token with default expiration
        token = user.generate_auth_token()
        u_id = User.verify_auth_token(token)
        self.assertEqual(u_id, user.id)

        u_id = User.verify_auth_token('BadToken')
        self.assertEqual(u_id, None)

        # sleep for 1 second to allow token to expire
        token = user.generate_auth_token(expires_in=1)
        time.sleep(2)
        u_id = User.verify_auth_token(token)
        self.assertEqual(u_id, None)

        # # Validate handling of bad signature
        # # with self.assertRaises(BadSignature):
        # with self.assertRaises(Exception) as e:
        #     User.verify_auth_token('BadToken')
        #
        #
        # # Create token with 20msec expiration
        # token = user.generate_auth_token(expires_in=20)
        # # sleep for 1 second to allow token to expire
        # time.sleep(10)
        # with self.assertRaises(SignatureExpired):
        #     User.verify_auth_token(token)


    # Support methods
    @staticmethod
    def createUser(password=password):
        # noinspection PyArgumentList
        return User(username=TestUser.username, email=TestUser.email,
                    password=password)

