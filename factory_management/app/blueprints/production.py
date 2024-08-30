from flask import Blueprint, request, jsonify
from app.models import db, Production
from flask_limiter.decorator import limiter_limit

production_bp = Blueprint('production', __name__)

@production_bp.route('/', methods=['POST'])
@limiter_limit("5 per minute")
def create_production():
    data = request.json
    new_production = Production(product_id=data['product_id'], quantity_produced=data['quantity_produced'], date_produced=data['date_produced'])
    db.session.add(new_production)
    db.session.commit()
    return jsonify({'id': new_production.id, 'product_id': new_production.product_id, 'quantity_produced': new_production.quantity_produced, 'date_produced': new_production.date_produced}), 201

@production_bp.route('/', methods=['GET'])
@limiter_limit("10 per minute")
def get_production():
    production = Production.query.all()
    return jsonify([{'id': prod.id, 'product_id': prod.product_id, 'quantity_produced': prod.quantity_produced, 'date_produced': prod.date_produced} for prod in production])
