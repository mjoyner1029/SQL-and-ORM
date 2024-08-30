from flask import Blueprint, request, jsonify
from app.models import db, Order
from flask_limiter.decorator import limiter_limit

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/', methods=['GET'])
@limiter_limit("10 per minute")
def get_orders():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    orders_paginated = Order.query.paginate(page, per_page, False)
    orders = [{
        'id': order.id,
        'customer_id': order.customer_id,
        'product_id': order.product_id,
        'quantity': order.quantity,
        'total_price': order.total_price
    } for order in orders_paginated.items]

    response = {
        'total': orders_paginated.total,
        'pages': orders_paginated.pages,
        'current_page': orders_paginated.page,
        'per_page': orders_paginated.per_page,
        'orders': orders
    }

    return jsonify(response)
