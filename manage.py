import os
from flask_script import Server, Manager
from flask import g
from catalog import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
manager.add_command("runserver", Server(host="0.0.0.0", port=5000))


@app.before_request
def before_request():
    from catalog.models import DBSession
    if not hasattr(g, 'db_session'):
        g.db_session = DBSession()


@app.teardown_appcontext
def close_session(error):
    if hasattr(g, 'db_session'):
        g.db_session.close()


@manager.command
def hello():
    print("Hello")


if __name__ == "__main__":
    manager.run()
