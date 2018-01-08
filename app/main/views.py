from flask import url_for, request, abort, g, render_template, flash
from flask import current_app, redirect
from sqlalchemy.exc import IntegrityError
from app import models
from . import main
from app import has_no_empty_params
from app.main.forms import CategoryForm, ItemForm
from app.models.category import Category
from app.models.item import Item
from flask_login import login_required, current_user
from secrets import google_client_secrets as gcs
from app import db
from app.auth.utils import redirect_back, get_redirect_target


@main.route('/', methods=['GET'], endpoint='homepage')
@main.route('/category/<category_id>', endpoint='home_itemlist')
def home(category_id=None):
    categories = Category.getAll()
    category = None

    # Category is not specified.  Show latest items
    if not category_id:
        items = Item.getItemsByDate()
    # Show items for specified category
    else:
        category_id = int(category_id)
        for category in categories:
            if category.id == category_id:
                break

        items = Item.getItemsByCategory(category_id=category_id)
    return render_template("home.html", categories=categories, items=items,
                           category=category)


@main.route('/item/<item_id>')
def displayItem(item_id):
    item = Item.getItemById(item_id)
    if not item:
        flash('Item {} not found'.format(item_id))
        return redirect('main.homepage')

    return render_template("item_details.html", item=item, user=current_user)


@main.route('/item/new', methods=['GET', 'POST'])
@login_required
def newitem():
    name = None
    description = None
    category = None
    next = get_redirect_target()
    form = ItemForm(next=next)
    form.category.choices = \
        [(category.id, category.name) for category in Category.getAll()]

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
        return redirect_back('main.homepage')

    return render_template('item_form.html', form=form, name=name,
                           description=description, category=category)


@main.route('/item/<item_id>/edit', methods=['GET', 'POST'])
@login_required
def editItem(item_id):
    item = Item.getItemById(item_id)
    if not item:
        flash("Item () note found").form(item_id)
        return redirect(url_for(main.homepage))

    next = get_redirect_target()
    form = ItemForm(next=next)
    form.category.choices = [(category.id, category.name)
                             for category in Category.getAll()]

    if request.method == 'GET':
        form.name.data = item.name
        form.description.data = item.description
        form.category.data = item.category_id
        form.category.choices = [(category.id, category.name)
                                 for category in Category.getAll()]
        return render_template('item_form.html', form=form, name=item.name,
                               description=item.description,
                               category=item.category)

    if form.validate_on_submit():
        item.name = form.data['name']
        item.description = form.data['description']
        cat_id = form.data['category']
        item.category_id = form.data['category']
        db.session.commit()
        return redirect_back('main.homepage')


@main.route('/item/<item_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteItem(item_id):
    # Validate item_id
    item = Item.getItemById(item_id)
    if not item:
        flash('Item {} not found'.format(item_id))
        return redirect_back('main.homepage')

    next = get_redirect_target()
    if request.method == 'POST':
        Item.delete(item_id)
        flash("{} deleted".format(item.name))
        return redirect(url_for('main.homepage'))
    else:
        return render_template('item_delete.html', item=item, next=next)


@main.route('/category/new', methods=['GET', 'POST'])
@login_required
def newcategory():
    form = CategoryForm()
    category_name = None
    if form.validate_on_submit():
        try:
            category_name = form.category_name.data.lower()
            Category.create(category_name)
            flash("{} Category created".format(category_name))
            return redirect(url_for('main.homepage'))
        except IntegrityError as e:
            flash("Error: Duplicate category: {} already exists".format(
                category_name))
            return render_template('item_form.html', form=form,
                                   name=category_name)
    return render_template('item_form.html', form=form, name=category_name)


# For development purposes.  Shows the static routes in the flask
# routing table
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
