from flask import Flask
from config import config
import json

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.models import init_app as models_init_app
    models_init_app(app)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else()
    arguments = rule.arguments if rule.arguments is not None else()
    return len(defaults) >= len(arguments)
