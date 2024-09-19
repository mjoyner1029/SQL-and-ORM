from flask import Blueprint, jsonify, request
from app.models import Production, db, Order, Product, Customer
from sqlalchemy import func

production = Blueprint('production', __name__)

@production.route('', methods=['POST'])
def create_production():
    data = request.get_json()
    production = Production(
        product_id=data['product_id'],
        quantity_produced=data['quantity_produced'],
        date_produced=data['date_produced']
    )
    db.session.add(production)
    db.session.commit()
    return jsonify({
        'id': production.id,
        'product_id': production.product_id,
        'quantity_produced': production.quantity_produced,
        'date_produced': production.date_produced
    }), 201

@production.route('', methods=['GET'])
def list_production():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    productions = Production.query.paginate(page, per_page, error_out=False)
    return jsonify({
        'items': [{
            'id': p.id,
            'product_id': p.product_id,
            'quantity_produced': p.quantity_produced,
            'date_produced': p.date_produced
        } for p in productions.items],
        'total': productions.total,
        'page': productions.page,
        'pages': productions.pages
    }), 200

@production.route('/employee-performance', methods=['GET'])
def employee_performance():
    subquery = (
        db.session.query(
            Order.employee_id,
            func.sum(Order.quantity).label('total_quantity')
        )
        .group_by(Order.employee_id)
        .subquery()
    )

    results = db.session.query(
        employees.name,
        func.coalesce(subquery.c.total_quantity, 0).label('total_quantity')
    ).outerjoin(subquery, employees.id == subquery.c.employee_id).all()

    return jsonify([{'employee': e.name, 'total_quantity': e.total_quantity} for e in results]), 200

@production.route('/top-selling-products', methods=['GET'])
def top_selling_products():
    results = db.session.query(
        Product.name,
        func.sum(Order.quantity).label('total_quantity')
    ).join(Order, Product.id == Order.product_id).group_by(Product.id).order_by(func.sum(Order.quantity).desc()).all()

    return jsonify([{'product': p.name, 'total_quantity': p.total_quantity} for p in results]), 200

@production.route('/customer-lifetime-value', methods=['GET'])
def customer_lifetime_value():
    threshold = 1000.0  # Example threshold

    results = db.session.query(
        Customer.name,
        func.sum(Order.total_price).label('total_order_value')
    ).join(Order, Customer.id == Order.customer_id).group_by(Customer.id).having(func.sum(Order.total_price) >= threshold).all()

    return jsonify([{'customer': c.name, 'total_order_value': c.total_order_value} for c in results]), 200

@production.route('/production-efficiency', methods=['GET'])
def production_efficiency():
    date = request.args.get('date')  # Expected format: YYYY-MM-DD

    subquery = (
        db.session.query(
            Production.product_id,
            func.sum(Production.quantity_produced).label('total_quantity')
        )
        .filter(Production.date_produced == date)
        .group_by(Production.product_id)
        .subquery()
    )

    results = db.session.query(
        Product.name,
        func.coalesce(subquery.c.total_quantity, 0).label('total_quantity')
    ).outerjoin(subquery, Product.id == subquery.c.product_id).all()

    return jsonify([{'product': p.name, 'total_quantity': p.total_quantity} for p in results]), 200
