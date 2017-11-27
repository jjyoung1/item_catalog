import os
import json

''' Google Client Secrets'''
class GoogleClientSecrets:

    gcs = None
    path = None
    def __init__(self, filename):
        self.path = os.path.join(basedir, filename)
        self.gcs = json.loads(
            open(self.path, 'r').read())

    def get_client_id(self):
        return self.gcs['web']['client_id']

    def get_secrets_path(self):
        return self.path

basedir = os.path.abspath(os.path.dirname(__file__)) + '/'

google_client_secrets = GoogleClientSecrets('client_secrets.json')

class FacebookClientSecrets:

    fcs = None
    path = None
    def __init__(self, filename):
        self.path = os.path.join(basedir, filename)
        self.fcs = json.loads(
            open(self.path, 'r').read())

    def get_client_id(self):
        return self.gcs['web']['client_id']

    def get_secrets_path(self):
        return self.path

facebook_client_secrets = FacebookClientSecrets('fb_client_secrets.json')
