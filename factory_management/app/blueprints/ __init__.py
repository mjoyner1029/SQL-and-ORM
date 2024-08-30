# app/blueprints/__init__.py

from flask import Blueprint

# Initialize all blueprints here if you want to avoid importing them in the main app module

# For example, importing blueprints
from .employees import employees_bp
from .products import products_bp
from .orders import orders_bp
from .customers import customers_bp
from .production import production_bp
from .analytics import analytics_bp
