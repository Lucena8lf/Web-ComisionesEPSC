from flask import render_template
from flask_login import current_user, login_user, logout_user

from app import login_manager
from . import auth_bp

# from .forms import SingupForm, LoginForm
from .models import Administrativo


@auth_bp.route("/login")
def login():
    return "Esta ruta es para que el administrativo haga el login"


# Hacemos el user_loader que no sirve nada más que para recoger la ID del usuario
# que está usando la aplicación
@login_manager.user_loader
def load_user(administrativo_id):
    return Administrativo.get_by_id(administrativo_id)
