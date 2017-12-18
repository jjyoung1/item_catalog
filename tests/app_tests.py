import unittest
from app import create_app, db
from flask import jsonify


class UITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # def test_no_categories(self):
    #     rv = self.app.get('/')
    #     assert b'No Categories'
