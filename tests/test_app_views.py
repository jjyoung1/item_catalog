import unittest
from app import create_app, db

class AppViewTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')

        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_no_categories(self):
        rv = self.client.get('/')
        self.assertEqual(rv.status_code , 200)
        self.assertTrue('Add a new category' in rv.get_data(as_text=True))
        self.assertTrue('Add a new item' in rv.get_data(as_text=True))
        self.assertTrue('No Categories' in rv.get_data(as_text=True))
        self.assertTrue('No Items' in rv.get_data(as_text=True))
