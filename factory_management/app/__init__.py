from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)

def create_app(config_filename='app/config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)
    
    db.init_app(app)
    limiter.init_app(app)
    
    from .blueprints import (
        employees_bp, products_bp, orders_bp, customers_bp, production_bp, analytics_bp
    )
    
    app.register_blueprint(employees_bp, url_prefix='/employees')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(orders_bp, url_prefix='/orders')
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(production_bp, url_prefix='/production')
    app.register_blueprint(analytics_bp, url_prefix='/analytics')
    
    return app
