from flask import Blueprint, redirect, url_for


base = Blueprint('base', __name__)

@base.route('/')
def index():
    return redirect(url_for('empleados.index'))