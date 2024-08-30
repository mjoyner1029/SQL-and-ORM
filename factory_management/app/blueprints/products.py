from flask import Blueprint, request, jsonify
from app.models import db, Product
from flask_limiter.decorator import limiter_limit

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
@limiter_limit("10 per minute")
def get_products():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    products_paginated = Product.query.paginate(page, per_page, False)
    products = [{'id': prod.id, 'name': prod.name, 'price': prod.price} for prod in products_paginated.items]
    
    response = {
        'total': products_paginated.total,
        'pages': products_paginated.pages,
        'current_page': products_paginated.page,
        'per_page': products_paginated.per_page,
        'products': products
    }

    return jsonify(response)
