#!/usr/bin/env python3
import os
import sys
import click

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

# from flask_script import Server, Manager
# from flask import g
from app import create_app, db
from flask import g

from app.models.category import Category
from app.models.item import Item
from app.models.user import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
ctx = app.app_context()
ctx.push()
db.create_all()
ctx.pop()


@app.shell_context_processor
def make_shell_context():
    ctx = dict(
        db=db,
        User=User,
        Category=Category,
        Item=Item,
    )
    return ctx


@app.cli.command()
@click.option('--coverage/--no-coverage', default=False,
              help='Run tests under code coverage.')
def test(coverage):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE'] = '1'
        sys.exit(subprocess.call(sys.argv))

    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()



# if __name__ == '__main__':
#     app.debug = True
#     app.run(host='0.0.0.0', port=5000)
