from app.models import db, Customer, Order
from sqlalchemy import func

def get_customer_lifetime_value(threshold=1000.0):
    query = db.session.query(
        Customer.name,
        func.sum(Order.total_price).label('total_order_value')
    ).join(Order, Customer.id == Order.customer_id) \
     .group_by(Customer.name) \
     .having(func.sum(Order.total_price) >= threshold).all()
    
    results = [{'customer_name': name, 'total_order_value': total_order_value} for name, total_order_value in query]
    
    return results
