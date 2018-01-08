from flask import Blueprint
from flask_httpauth import HTTPBasicAuth

auth = Blueprint('auth', __name__)
basic_auth = HTTPBasicAuth()

import app.auth.views
