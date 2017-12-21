from flask import jsonify

# TODO: Fix and enable User REST methods
# @main.route('/users', methods=['POST'])
# def new_user():
#     username = request.json.get('username')
#     password = request.json.get('password')
#     email = request.json.get('email')
#     if username is None or password is None:
#         print("missing arguments")
#         abort(400)
#
#     models.User.create(username, password, email)
#
#     if db.session.query(models.User).filter_by(username=username).first() is not None:
#         print("existing user")
#         user = db.session.query(models.User).filter_by(username=username).first()
#         return jsonify({
#             'message': 'user already exists'}), 200  # , {'Location': url_for('get_user', id = user.id, _external = True)}
#
#     user = models.User(username=username)
#     user.hash_password(password)
#     db.session.add(user)
#     db.session.commit()
#
#     return jsonify(
#         {'username': user.username}), 201  # , {'Location': url_for('get_user', id = user.id, _external = True)}
#

# @main.route('/users/<int:id>')
# def get_user(id):
#     user = db.session.query(models.User).filter_by(id=id).one()
#     if not user:
#         abort(400)
#     return jsonify(user.serialize)
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
