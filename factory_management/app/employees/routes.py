from flask import Blueprint, jsonify, request
from app.models import Employee, db

employees = Blueprint('employees', __name__)

@employees.route('', methods=['POST'])
def create_employee():
    data = request.get_json()
    employee = Employee(name=data['name'], position=data['position'])
    db.session.add(employee)
    db.session.commit()
    return jsonify({'id': employee.id, 'name': employee.name, 'position': employee.position}), 201

@employees.route('', methods=['GET'])
def list_employees():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    employees = Employee.query.paginate(page, per_page, error_out=False)
    return jsonify({
        'items': [{'id': e.id, 'name': e.name, 'position': e.position} for e in employees.items],
        'total': employees.total,
        'page': employees.page,
        'pages': employees.pages
    }), 200
