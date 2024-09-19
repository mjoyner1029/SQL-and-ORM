from flask import Blueprint, jsonify, request
from app.models import Product, db

inventory = Blueprint('inventory', __name__)

@inventory.route('', methods=['POST'])
def create_product():
    data = request.get_json()
    product = Product(name=data['name'], price=data['price'])
    db.session.add(product)
    db.session.commit()
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price}), 201

@inventory.route('', methods=['GET'])
def list_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    products = Product.query.paginate(page, per_page, error_out=False)
    return jsonify({
        'items': [{
            'id': p.id,
            'name': p.name,
            'price': p.price
        } for p in products.items],
        'total': products.total,
        'page': products.page,
        'pages': products.pages
    }), 200
