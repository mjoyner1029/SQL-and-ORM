from flask import Blueprint, request, jsonify
from app.models import db, Employee
from flask_limiter.decorator import limiter_limit

employees_bp = Blueprint('employees', __name__)

@employees_bp.route('/', methods=['POST'])
@limiter_limit("5 per minute")
def create_employee():
    data = request.json
    new_employee = Employee(name=data['name'], position=data['position'])
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({'id': new_employee.id, 'name': new_employee.name, 'position': new_employee.position}), 201

@employees_bp.route('/', methods=['GET'])
@limiter_limit("10 per minute")
def get_employees():
    employees = Employee.query.all()
    return jsonify([{'id': emp.id, 'name': emp.name, 'position': emp.position} for emp in employees])
