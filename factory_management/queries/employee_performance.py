from app.models import db, Employee, Production
from sqlalchemy import func

def get_employee_performance():
    query = db.session.query(
        Employee.name,
        func.sum(Production.quantity_produced).label('total_quantity')
    ).join(Production, Employee.id == Production.product_id) \
     .group_by(Employee.name).all()
    
    results = [{'employee_name': name, 'total_quantity': total_quantity} for name, total_quantity in query]
    
    return results
