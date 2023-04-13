from flask import Blueprint

comision_bp = Blueprint("comision", __name__, template_folder="templates")

from . import routes
