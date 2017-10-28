import json
import random
import string

import httplib2  # http client library
import requests  # http library
from flask import render_template, request, make_response, abort, flash
from flask import session as login_session
# from apiclient import discovery
from oauth2client import client

from . import auth

CLIENT_ID = json.loads(
    open('../client_secrets.json', 'r').read())['web']['client_id']

@auth.route('/login2')
def login2():
    return "Called login2"

@auth.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template("auth/login.html", STATE=state)

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
    CLIENT_SECRET_FILE = '../client_secrets.json'

    # Exchange auth code for access token, refresh token, and ID token
    credentials = client.credentials_from_clientsecrets_and_code(
        CLIENT_SECRET_FILE,
        ['profile', 'email'],
        auth_code)

    # Call Google API
    # http_auth = credentials.authorize(httplib2.Http())

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    # try:
    #     # Upgrade the authorization code into a credentials object
    #     oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
    #     oauth_flow.redirect_uri = 'postmessage'
    #     credentials = oauth_flow.step2_exchange(code)
    # except FlowExchangeError:
    #     response = make_response(json.dumps('Failed to upgrade the'
    #                                         'authorization code.'), 401)
    #     response.headers['Content-Type'] = 'application/json'
    #     return response
    #

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token
    h = httplib2.Http()
    # resp = h.request(url, 'GET')[1].decode("utf-8")
    result = json.loads(h.request(url, 'GET')[1].decode("utf-8"))
    # result = json.loads(h.request(url, 'GET')[1].decode("utf-8"))

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
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    data = answer.json()

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token

    # Get profile info from ID token
    login_session['google_id'] = credentials.id_token['sub']
    login_session['email'] = credentials.id_token['email']
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output  # ADD @auth.verify_password decorator here


@auth.route("/gdisconnect")
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get("access_token")
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Execute HTTP Get request to revoke current token.
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        del login_session['access_token']
        del login_session['google_id']
        del login_session['username']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user'),
                                 400)
        response.headers = 'application/json'
        return response

