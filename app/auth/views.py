import json
import random
import string

import httplib2  # http client library
import requests  # http library
from flask import render_template, request, make_response, abort, flash, \
    redirect, url_for, g
from flask import session as login_session, jsonify
from flask_login import LoginManager, login_user, logout_user, current_user
from oauth2client import client

from app.models.user import User
from app.auth import auth, basic_auth
from app.auth.utils import redirect_back, get_redirect_target
from app import login_manager
from secrets import google_client_secrets as gcs, \
    facebook_client_secrets as fbcs

from app import db
from app.auth.forms import LoginForm, RegistrationForm

CLIENT_ID = gcs.get_client_id()


@basic_auth.verify_password
def verify_password(username_or_token, password):
    # Check if a valid token was passed
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = db.session.query(User).filter_by(id=user_id).one()
    else:
        # Attempt to get user from DB
        user = db.session.query(User).filter_by(
            username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False  # Return invalid user
    g.user = user
    return True  # Return valid user


# add /token route here to get a token for a user with login credentials
@auth.route('/token')
@basic_auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@auth.route('/register', methods=['GET', 'POST'])
def register():
    # state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    # login_session['state'] = state
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    picture=url_for('static', filename='img/generic_user.jpg',
                                    _external=True))
        db.session.add(user)
        flash('Account Created')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)  # , State=state)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for x in
        range(32))
    login_session['state'] = state
    next = get_redirect_target()
    form = LoginForm(next=next)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me)
            login_session['picture'] = user.picture
            return redirect_back('main.homepage')
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form, state=state)


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    if not current_user.is_authenticated:
        flash("You are not logged in")
        return redirect(url_for('main.homepage'))
    else:
        logout_user()
        if login_session.get('picture'):
            del login_session['picture']

        provider = login_session.get('provider')
        if provider == 'google':
            gdisconnect()
        elif provider == 'facebook':
            fbdisconnect()

        return redirect(url_for('main.homepage'))


@auth.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    auth_code = request.data

    # If this request does not have `X-Requested-With` header, this could be a CSRF
    if not request.headers.get('X-Requested-With'):
        abort(403)

    # Set path to the Web application client_secret_*.json file you downloaded from the
    # Google API Console: https://console.developers.google.com/apis/credentials
    CLIENT_SECRET_FILE = gcs.get_secrets_path()  # '/secrets/client_secrets.json'

    # Exchange auth code for access token, refresh token, and ID token
    credentials = client.credentials_from_clientsecrets_and_code(
        CLIENT_SECRET_FILE,
        ['profile', 'email'],
        auth_code)

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode("utf-8"))

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    google_id = credentials.id_token['sub']
    if result['user_id'] != google_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')

    stored_google_id = login_session.get('google_id')
    if stored_access_token is not None and google_id == stored_google_id:
        response = make_response(
            json.dumps('Current user is already connected.'),
            200)
        response.headers['Content-Type'] = 'application/json'
        return response

    data = answer.json()

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['provider'] = 'google'

    # Get profile info from ID token
    login_session['google_id'] = credentials.id_token['sub']
    email = credentials.id_token['email']
    login_session['picture'] = data['picture']

    user_id = User.getID(email)

    # If user does not exist, then it is created with a disabled password
    # After this, login is not possible using the site login page until
    # a valid password is specified
    # TODO: enable password setting and changing
    if not user_id:
        user = User()
        user.username = data['name']
        user.password = ''
        user.email = email
        user.picture = None
        db.session.add(user)
        db.session.commit()
        user_id = User.getID(email)

    user = User.getInfo(user_id)
    login_user(user)
    return redirect(url_for('main.homepage'))


def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get("access_token")
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Execute HTTP Get request to revoke current token.
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    # Even if failure occurred, we want to delete the google access token and
    # id from session
    del login_session['access_token']
    del login_session['google_id']
    del login_session['provider']

    if result['status'] != '200':
        flash("Failed to revoke google token for given user")
    return


@auth.route('/fbconnect', methods=['POST'])
def fbconnect():
    if (request.args.get('state')) != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data.decode()

    # Exchange client token for long-lived server-side token
    app_id = json.loads(open(fbcs.get_secrets_path(), 'r').read())['web'][
        'app_id']
    app_secret = json.loads(open(fbcs.get_secrets_path(), 'r').read())['web'][
        'app_secret']
    url = 'https://graph.facebook.com/v2.10/oauth/' \
          'access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s' \
          '&fb_exchange_token=%s' % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result.decode())

    # Use token to get user info from API
    token = "access_token=" + data['access_token']
    url = 'https://graph.facebook.com/v2.9/me?%s&fields=name,id,email,picture' \
          % token

    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    print("url sent for API access:%s" % url)
    print("API JSON reuslt: %s" % result)
    data = json.loads(result.decode())
    login_session['provider'] = 'facebook'
    login_session['facebook_id'] = data['id']
    login_session['picture'] = data['picture']['data']['url']
    login_session['access_token'] = access_token

    # see if user exists, if it doesn't make a new one
    user_id = User.getID(data['email'])
    if not user_id:
        user = User()
        user.username = data['username']
        user.password = ''
        user.email = data['email']
        user.picture = None
        db.session.add(user)
        db.session.commit()
        user_id = User.getID(data['email'])

    user = User.getInfo(user_id)
    login_user(user)
    flash("you are now logged in as %s" % user.username)
    return redirect(url_for('main.homepage'))


def fbdisconnect():
    facebook_id = login_session.get('facebook_id')
    # The access token must be included to successfully logout
    access_token = login_session.get('access_token')

    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % \
          (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]

    del login_session['provider']
    del login_session['facebook_id']
    del login_session['access_token']
    return redirect(url_for('main.homepage'))


@login_manager.user_loader
def load_user(user_id):
    return User.getInfo(user_id)


def init_app(app):
    ''''''
