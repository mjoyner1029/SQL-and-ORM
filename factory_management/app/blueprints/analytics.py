from flask import Blueprint, request, jsonify
from app.queries.employee_performance import get_employee_performance
from app.queries.top_selling_products import get_top_selling_products
from app.queries.customer_lifetime_value import get_customer_lifetime_value
from app.queries.production_efficiency import get_production_efficiency

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/employee-performance', methods=['GET'])
def employee_performance():
    data = get_employee_performance()
    return jsonify(data)

@analytics_bp.route('/top-selling-products', methods=['GET'])
def top_selling_products():
    data = get_top_selling_products()
    return jsonify(data)

@analytics_bp.route('/customer-lifetime-value', methods=['GET'])
def customer_lifetime_value():
    threshold = request.args.get('threshold', default=1000.0, type=float)
    data = get_customer_lifetime_value(threshold)
    return jsonify(data)

@analytics_bp.route('/production-efficiency', methods=['GET'])
def production_efficiency():
    date = request.args.get('date')
    data = get_production_efficiency(date)
    return jsonify(data)
