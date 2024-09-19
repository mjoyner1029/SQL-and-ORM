from flask import Flask
from app.models import db
from app.extensions import limiter
from app.employees.routes import employees
from app.production.routes import production
from app.inventory.routes import inventory

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    limiter.init_app(app)

    app.register_blueprint(employees, url_prefix='/employees')
    app.register_blueprint(production, url_prefix='/production')
    app.register_blueprint(inventory, url_prefix='/products')

    return app
