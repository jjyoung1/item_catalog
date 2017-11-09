import json  # Lib: Convert in-memory python objects to a serialized representation in json

from flask import url_for, jsonify, request, abort, g

from flask_httpauth import HTTPBasicAuth
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app import has_no_empty_params
from . import main

# Converts return value from a function into a real response
#    object that can be sent to the client

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

auth = HTTPBasicAuth()

# engine = create_engine('sqlite:///item_catalog.db')
# models.Base.metadata.bind = engine
#
# DBSession = sessionmaker(bind=engine)
# db_session = DBSession()


@auth.verify_password
def verify_password(username_or_token, password):
    # Check if a valid token was passed
    user_id = models.User.verify_auth_token(username_or_token)
    if user_id:
        user = g.db_session.query(models.User).filter_by(id=user_id).one()
    else:
        # Attempt to get user from DB
        user = g.db_session.query(models.User).filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False  # Return invalid user
    g.user = user
    return True  # Return valid user


# add /token route here to get a token for a user with login credentials
@main.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@main.route('/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    if username is None or password is None:
        print("missing arguments")
        abort(400)

    models.User.create(username, password, email)

    if g.db_session.query(models.User).filter_by(username=username).first() is not None:
        print("existing user")
        user = g.db_session.query(models.User).filter_by(username=username).first()
        return jsonify({
            'message': 'user already exists'}), 200  # , {'Location': url_for('get_user', id = user.id, _external = True)}

    user = models.User(username=username)
    user.hash_password(password)
    g.db_session.add(user)
    g.db_session.commit()
    return jsonify(
        {'username': user.username}), 201  # , {'Location': url_for('get_user', id = user.id, _external = True)}


@main.route('/users/<int:id>')
def get_user(id):
    user = g.db_session.query(models.User).filter_by(id=id).one()
    if not user:
        abort(400)
    return jsonify({'username': user.username})


@main.route('/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


@main.route('/products', methods=['GET', 'POST'])
@auth.login_required
def showAllProducts():
    if request.method == 'GET':
        products = g.db_session.query(models.Product).all()
        return jsonify(products=[p.serialize for p in products])
    if request.method == 'POST':
        name = request.json.get('name')
        category = request.json.get('category')
        price = request.json.get('price')
        newItem = models.Product(name=name, category=category, price=price)
        g.db_session.add(newItem)
        g.db_session.commit()
        return jsonify(newItem.serialize)


@main.route('/products/<category>')
@auth.login_required
def showCategoriedProducts(category):
    if category == 'fruit':
        fruit_items = g.db_session.query(models.Product).filter_by(category='fruit').all()
        return jsonify(fruit_products=[f.serialize for f in fruit_items])
    if category == 'legume':
        legume_items = g.db_session.query(models.Product).filter_by(category='legume').all()
        return jsonify(legume_products=[l.serialize for l in legume_items])
    if category == 'vegetable':
        vegetable_items = g.db_session.query(models.Product).filter_by(category='vegetable').all()
        return jsonify(produce_products=[p.serialize for p in vegetable_items])


@main.route('/', methods=['GET'])
def home():
    return ("Hello There")

@main.route("/site-map")
def site_map():
    links = []
    for rule in main.url_map.iter_rules():

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


def init_app(app):
    ''''''
