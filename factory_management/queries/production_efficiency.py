from app.models import db, Product, Production
from sqlalchemy import func

def get_production_efficiency(date):
    subquery = db.session.query(
        Production.product_id,
        func.sum(Production.quantity_produced).label('total_quantity')
    ).filter(Production.date_produced == date) \
     .group_by(Production.product_id).subquery()
    
    query = db.session.query(
        Product.name,
        func.coalesce(subquery.c.total_quantity, 0).label('total_quantity_produced')
    ).outerjoin(subquery, Product.id == subquery.c.product_id) \
     .order_by(Product.name).all()
    
    results = [{'product_name': name, 'total_quantity_produced': total_quantity_produced} for name, total_quantity_produced in query]
    
    return results
