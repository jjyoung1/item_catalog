import os
# from flask_script import Server, Manager
# from flask import g
from app import create_app
from flask import g

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
foo="Hi there"

# @app.route('/')
# def index():
#     return '<h1>Hello</h1'

@app.before_request
def before_request():
    from app.models import DBSession
    if not hasattr(g, 'db_session'):
        g.db_session = DBSession()


@app.teardown_appcontext
def close_session(error):
    if hasattr(g, 'db_session'):
        g.db_session.close()

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
