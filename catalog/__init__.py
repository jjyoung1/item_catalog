from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_login import LoginManager
from config import config
import json

bootstrap = Bootstrap()
moment = Moment()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)

    from catalog.models import init_app as models_init_app
    models_init_app(app)

    from catalog.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from catalog.auth import auth as auth_blueprint
    from catalog.auth.views import init_app as auth_init_app
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    auth_init_app(app)
    login_manager.init_app(app)

    return app

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else()
    arguments = rule.arguments if rule.arguments is not None else()
    return len(defaults) >= len(arguments)
