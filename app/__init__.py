import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager
import json

from config import config


bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# basedir = os.path.abspath(os.path.dirname(__file__))

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    # from app.models import init_app as models_init_app
    # models_init_app(app)

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


