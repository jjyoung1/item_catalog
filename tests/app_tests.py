# import os
# import app
# import unittest
# import tempfile
#
# class AppTestCase(unittest.TestCase):
#
#     def setup(self):
#         self.db_fd, app.config['SQLALCHEMY_DATABASE_URI'] = tempfile.mkstemp()
#         app.testing = True
#         self.app = app.test_client()
