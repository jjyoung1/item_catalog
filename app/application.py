import json

from flask import Flask, url_for, g

from app.config import config

CLIENT_ID = json.loads(
    open('../client_secrets.json', 'r').read())['web']['client_id']

app = Flask(__name__)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else()
    arguments = rule.arguments if rule.arguments is not None else()
    return len(defaults) >= len(arguments)

@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():

        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    str = ''
    str += '<h1>url rules</h1>'
    str += '<ul>'
    for link in links:
        url, func = link
        str += "<li>"\
               + url + ': ' + func + \
        "</li>"

    str += '</ul>'
    return str


def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.models import init_app as models_init_app
    models_init_app(app)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app

@app.before_request
def before_request():
    from app.models import DBSession
    if not hasattr(g,'db_session'):
        g.db_session = DBSession()

@app.teardown_appcontext
def close_session(error):
    from app.models import DBSession
    if hasattr(g,'db_session'):
        g.db_session.close()


if __name__ == '__main__':
    config_name = 'default'

    create_app(config_name)
    app.run(host='0.0.0.0', port=5000)
