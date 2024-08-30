from flask import Blueprint, request, jsonify
from app.models import db, Customer
from flask_limiter.decorator import limiter_limit

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/', methods=['POST'])
@limiter_limit("5 per minute")
def create_customer():
    data = request.json
    new_customer = Customer(name=data['name'], email=data['email'], phone=data['phone'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'id': new_customer.id, 'name': new_customer.name, 'email': new_customer.email, 'phone': new_customer.phone}), 201

@customers_bp.route('/', methods=['GET'])
@limiter_limit("10 per minute")
def get_customers():
    customers = Customer.query.all()
    return jsonify([{'id': cust.id, 'name': cust.name, 'email': cust.email, 'phone': cust.phone} for cust in customers])
