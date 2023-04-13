from flask import Blueprint

informe_bp = Blueprint("informe", __name__, template_folder="templates")

from . import routes
