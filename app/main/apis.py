from flask import jsonify, request
from app import db
# from app import main
from app.models.item import Item
from flask_login import login_required
from . import main


@main.route('/api/catalog')
def getCatalog():
    items = db.session.query(Item).all()
    return jsonify(items=[i.serialize for i in items])

@main.route('/api/item/<item_id>')
def getItem(item_id):
    item = Item.getItemById(item_id)
    if not item:
        return jsonify("Item Not Found")
    else:
        return jsonify(item.serialize)
