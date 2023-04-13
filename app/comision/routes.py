from flask import render_template

from . import comision_bp

from .models import Comision


@comision_bp.route("/comisiones")
def comisiones():
    return "Esta ruta obtiene todas las comisiones"
