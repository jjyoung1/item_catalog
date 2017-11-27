import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_login import LoginManager
from config import config
import json
from secrets import google_client_secrets as gcs


bootstrap = Bootstrap()
moment = Moment()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

basedir = os.path.abspath(os.path.dirname(__file__))
CLIENT_ID = gcs.get_client_id()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)

    from app.models import init_app as models_init_app
    models_init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import auth as auth_blueprint
    from app.auth.views import init_app as auth_init_app
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    auth_init_app(app)
    login_manager.init_app(app)

    return app

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else()
    arguments = rule.arguments if rule.arguments is not None else()
    return len(defaults) >= len(arguments)
