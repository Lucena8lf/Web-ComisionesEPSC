from flask import render_template

from . import informe_bp

from .models import Informe


@informe_bp.route("/informes")
def informes():
    return "Esta ruta es para crear un informe"
