import unittest
from app import create_app, db
import db_functions as dbf
import html

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

    def test_categories(self):
        dbf.category_init()
        rv = self.client.get('/')
        for c in dbf.category_list:
            self.assertTrue(c in rv.get_data(as_text=True))

# TODO: fix comparisions related to Jinja encode/decode
    def test_items(self):
        dbf.category_init()
        dbf.item_init()
        rv = self.client.get('/')
        for i in dbf.item_list:
            i_name = html.escape(i['name'])
            self.assertTrue(i['name'] in rv.get_data(as_text=True))

