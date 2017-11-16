import os
import catalog
import unittest
import tempfile

class AppTestCase(unittest.TestCase):

    def setup(self):
        self.db_fd, catalog.config['SQLALCHEMY_DATABASE_URI'] = tempfile.mkstemp()
        catalog.testing = True
        self.app = catalog.test_client()
