# import json  # Lib: Convert in-memory python objects to a serialized representation in json

from flask import url_for, request, abort, g, render_template, flash
from flask import current_app, redirect

from sqlalchemy.exc import IntegrityError

from app import models
# from app import has_no_empty_params
from . import main
from .. import has_no_empty_params
from .forms import CategoryForm, ItemForm
from ..models.category import Category
from ..models.item import Item
from flask_login import login_required
from secrets import google_client_secrets as gcs
from .. import db


# Converts return value from a function into a real response
#    object that can be sent to the client

# CLIENT_ID = gcs.get_client_id()

@main.route('/', methods=['GET'], endpoint='homepage')
@main.route('/cathome/<category_id>', endpoint='home_itemlist')
def home(category_id=None):
    # categories = db.session.query(Category).order_by('name').all()
    categories = Category.getAll()
    category = None
    # # Convert list of Category objects in map of categories with the id being the key
    # c_map = dict([(k,v) for k,v in ((c.id, c.name) for c in categories)])

    if not category_id:
        items = Item.getItemsByDate()
    else:
        # category_id = db.session.query(Category).filter_by(id=cat_id).one()
        category_id = int(category_id)
        for category in categories:
            if category.id == category_id:
                break

        # category_name = categories[c
        # items = db.session.query(Item).filter_by(category_id=category_id).order_by('name')
        items = Item.getItemsByCategory(category_id=category_id)
    return render_template("home.html", categories=categories, items=items, category=category)


@main.route('/newitem', methods=['GET', 'POST'])
@login_required
def newitem():
    name = None
    description = None
    category = None
    form = ItemForm()
    form.category.choices = \
        [(category.id, category.name) for category in Category.getAll()]
        #[('1', 'Kitchen'), ('2', 'Landscaping')]

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        category_id = form.category.data
        item = Item(name=name,
                    description=description,
                    category_id=category_id)
        db.session.add(item)
        db.session.commit()
        flash("Item {} created".format(name))
        return redirect(url_for('main.homepage'))

    return render_template('item_form.html', form=form, name=name, description=description, category=category)


@main.route('/newcategory', methods=['GET', 'POST'])
@login_required
def newcategory():
    form = CategoryForm()
    category_name = None
    if form.validate_on_submit():
        try:
            category_name = form.category_name.data
            Category.create(category_name)
            flash("{} Category created".format(category_name))
            return redirect(url_for('main.homepage'))
        except IntegrityError as e:
            flash("Error: Duplicate category: {} already exists".format(category_name))
            return render_template('item_form.html', form=form, name=category_name)
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
