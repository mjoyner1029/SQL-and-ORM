from app.models import db, Product, Order
from sqlalchemy import func

def get_top_selling_products():
    query = db.session.query(
        Product.name,
        func.sum(Order.quantity).label('total_quantity_ordered')
    ).join(Order, Product.id == Order.product_id) \
     .group_by(Product.name) \
     .order_by(func.sum(Order.quantity).desc()).all()
    
    results = [{'product_name': name, 'total_quantity_ordered': total_quantity_ordered} for name, total_quantity_ordered in query]
    
    return results
