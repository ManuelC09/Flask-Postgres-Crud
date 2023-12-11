from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object('config.ProductionConfig')


db = SQLAlchemy(app)

from App.views import base
from App.Empleados.views import empleados

app.register_blueprint(base)
app.register_blueprint(empleados)


with app.app_context():
    db.create_all()