from flask import render_template

from flask_login import login_required, current_user

from . import main_bp


@main_bp.route("/")
@login_required
def index():
    """
    Ruta para la página de inicio
    """
    return render_template("main/index.html", current_user=current_user)
