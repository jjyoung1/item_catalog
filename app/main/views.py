# import json  # Lib: Convert in-memory python objects to a serialized representation in json

from flask import url_for, jsonify, request, abort, g, render_template, flash
from flask import current_app, redirect

# from flask_httpauth import HTTPBasicAuth
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from app import models
# from app import has_no_empty_params
from . import main
from .forms import CategoryForm, ItemForm
from ..models import Category
from flask_login import login_required
from secrets import google_client_secrets as gcs
from .. import db

# Converts return value from a function into a real response
#    object that can be sent to the client

CLIENT_ID = gcs.get_client_id()


@main.route('/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    if username is None or password is None:
        print("missing arguments")
        abort(400)

    models.User.create(username, password, email)

    if db.session.query(models.User).filter_by(username=username).first() is not None:
        print("existing user")
        user = db.session.query(models.User).filter_by(username=username).first()
        return jsonify({
            'message': 'user already exists'}), 200  # , {'Location': url_for('get_user', id = user.id, _external = True)}

    user = models.User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(
        {'username': user.username}), 201  # , {'Location': url_for('get_user', id = user.id, _external = True)}


# @main.route('/users/<int:id>')
# def get_user(id):
#     user = db.session.query(models.User).filter_by(id=id).one()
#     if not user:
#         abort(400)
#     return jsonify({'username': user.username})
#

# @main.route('/resource')
# @basic_auth.login_required
# def get_resource():
#     return jsonify({'data': 'Hello, %s!' % g.user.username})
#

# @main.route('/products', methods=['GET', 'POST'])
# @auth.login_required
# def showAllProducts():
#     if request.method == 'GET':
#         products = db.session.query(models.Product).all()
#         return jsonify(products=[p.serialize for p in products])
#     if request.method == 'POST':
#         name = request.json.get('name')
#         category = request.json.get('category')
#         price = request.json.get('price')
#         newItem = models.Product(name=name, category=category, price=price)
#         db.session.add(newItem)
#         db.session.commit()
#         return jsonify(newItem.serialize)
#

@main.route('/', methods=['GET'])
def home():
    return render_template("home.html")


@main.route('/newitem', methods=['GET', 'POST'])
def newitem():
    name = None
    description = None
    category = None
    form = ItemForm()
    form.category.choices = [('1', 'Kitchen'), ('2', 'Landscaping')]
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        category = form.category.data
        flash("Item {} created".format(name))
        return redirect(url_for('main.home'))
    return render_template('item_form.html', form=form, name=name, description=description, category=category)


@main.route('/newcategory', methods=['GET', 'POST'])
@login_required
def newcategory():
    form = CategoryForm()
    category_name = None
    if form.validate_on_submit():
        try:
            category_name = form.category_name.data
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()
            flash("{} Category created".format(category_name))
            return redirect(url_for('main.home'))
        except IntegrityError as e:
            print(type(e))
            print(e.args)
            print(e)
            flash("Error: Duplicate category: {} already exists".format(category_name))
    return render_template('item_form.html', form=form, name=category_name)


@main.route("/site-map")
def site_map():
    links = []
    for rule in current_app.url_map.iter_rules():

        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    str = ''
    str += '<h1>url rules</h1>'
    str += '<ul>'
    for link in links:
        url, func = link
        str += "<li>" \
               + url + ': ' + func + \
               "</li>"

    str += '</ul>'
    return str


def init_app(app):
    ''''''
