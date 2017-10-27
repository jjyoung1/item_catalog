from flask import render_template
from flask import session as login_session

from . import auth
from models import User
import random, string

@auth.route('/login2')
def login2():
    return "Called login2"

@auth.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template("auth/login.html", STATE=state)
