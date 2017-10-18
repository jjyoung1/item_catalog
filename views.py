from models import Base, User, Product
from flask import Flask, jsonify, render_template, request, url_for, abort, g, flash
from flask_httpauth import HTTPBasicAuth
from flask import session as login_session

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
import random, string

# Imports for oauth
from apiclient import discovery
from oauth2client import client
import httplib2  # http client library
import json  # Lib: Convert in-memory python objects to a serialized representation in json

# Converts return value from a function into a real response
#    object that can be sent to the client
from flask import make_response
import requests  # http library

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

from config import config

auth = HTTPBasicAuth()

engine = create_engine('sqlite:///item_catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template("login.html", STATE=state)


@app.route('/gconnect', methods=['POST'])
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
    CLIENT_SECRET_FILE = 'client_secrets.json'

    # Exchange auth code for access token, refresh token, and ID token
    credentials = client.credentials_from_clientsecrets_and_code(
        CLIENT_SECRET_FILE,
        ['profile', 'email'],
        auth_code)

    # Call Google API
    http_auth = credentials.authorize(httplib2.Http())

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['credentials'] = credentials.to_json()
    # drive_service = discovery.build('drive', 'v3', http=http_auth)
    # appfolder = drive_service.files().get(fileId='appfolder').execute()

    # Get profile info from ID token
    login_session['userid'] = credentials.id_token['sub']
    login_session['email'] = credentials.id_token['email']
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']

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
    #     # Check that the access token is valid.
    #     access_token = credentials.access_token
    #     url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
    #            % access_token)
    #     h = httplib2.Http()
    #     result = json.loads(h.request(url, 'GET')[1])
    #     # If there was an error in the access token info, abort.
    #     if result.get('error') is not None:
    #         response = make_response(json.dumps(result.get('error')), 500)
    #         response.headers['Content-Type'] = 'application/json'
    #         return response
    #
    #     # Verify that the access token is used for the intended user.
    #     gplus_id = credentials.id_token['sub']
    #     if result['user_id'] != gplus_id:
    #         response = make_response(
    #             json.dumps("Token's user ID doesn't match given user ID."), 401)
    #         response.headers['Content-Type'] = 'application/json'
    #         return response
    #
    #     # Verify that the access token is valid for this app.
    #     if result['issued_to'] != CLIENT_ID:
    #         response = make_response(
    #             json.dumps("Token's client ID does not match app's."), 401)
    #         print("Token's client ID does not match app's.")
    #         response.headers['Content-Type'] = 'application/json'
    #         return response
    #
    #     stored_access_token = login_session.get('access_token')
    #     stored_gplus_id = login_session.get('gplus_id')
    #     if stored_access_token is not None and gplus_id == stored_gplus_id:
    #         response = make_response(json.dumps('Current user is already connected.'),
    #                                  200)
    #         response.headers['Content-Type'] = 'application/json'
    #         return response
    #
    #     # Store the access token in the session for later use.
    #     login_session['access_token'] = credentials.access_token
    #     login_session['gplus_id'] = gplus_id
    #
    #     # Get user info
    #     userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    #     params = {'access_token': credentials.access_token, 'alt': 'json'}
    #     answer = requests.get(userinfo_url, params=params)
    #
    #     data = answer.json()
    #
    #     login_session['username'] = data['name']
    #     login_session['picture'] = data['picture']
    #     login_session['email'] = data['email']

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

@auth.verify_password
def verify_password(username_or_token, password):
    # Check if a valid token was passed
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
    else:
        # Attempt to get user from DB
        user = session.query(User).filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False  # Return invalid user
    g.user = user
    return True  # Return valid user


# add /token route here to get a token for a user with login credentials
@app.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@app.route('/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        print("missing arguments")
        abort(400)

    if session.query(User).filter_by(username=username).first() is not None:
        print("existing user")
        user = session.query(User).filter_by(username=username).first()
        return jsonify({
            'message': 'user already exists'}), 200  # , {'Location': url_for('get_user', id = user.id, _external = True)}

    user = User(username=username)
    user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify(
        {'username': user.username}), 201  # , {'Location': url_for('get_user', id = user.id, _external = True)}


@app.route('/users/<int:id>')
def get_user(id):
    user = session.query(User).filter_by(id=id).one()
    if not user:
        abort(400)
    return jsonify({'username': user.username})


@app.route('/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


@app.route('/products', methods=['GET', 'POST'])
@auth.login_required
def showAllProducts():
    if request.method == 'GET':
        products = session.query(Product).all()
        return jsonify(products=[p.serialize for p in products])
    if request.method == 'POST':
        name = request.json.get('name')
        category = request.json.get('category')
        price = request.json.get('price')
        newItem = Product(name=name, category=category, price=price)
        session.add(newItem)
        session.commit()
        return jsonify(newItem.serialize)


@app.route('/products/<category>')
@auth.login_required
def showCategoriedProducts(category):
    if category == 'fruit':
        fruit_items = session.query(Product).filter_by(category='fruit').all()
        return jsonify(fruit_products=[f.serialize for f in fruit_items])
    if category == 'legume':
        legume_items = session.query(Product).filter_by(category='legume').all()
        return jsonify(legume_products=[l.serialize for l in legume_items])
    if category == 'vegetable':
        vegetable_items = session.query(Product).filter_by(category='vegetable').all()
        return jsonify(produce_products=[p.serialize for p in vegetable_items])


@app.route('/', methods=['GET'])
def home():
    return ("Hello There")


if __name__ == '__main__':
    config_name = 'default'
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from models import init_app as models_init_app

    models_init_app(app)

    app.run(host='0.0.0.0', port=5000)
