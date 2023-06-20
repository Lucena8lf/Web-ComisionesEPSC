from flask import Blueprint

miembro_bp = Blueprint("miembro", __name__, template_folder="templates")

from . import routes
