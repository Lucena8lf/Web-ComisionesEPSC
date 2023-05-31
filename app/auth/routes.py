from flask import render_template, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import login_manager
from . import auth_bp

from .models import Administrativo

from .forms import LoginForm


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    error = None

    if form.validate_on_submit():
        administrativo = Administrativo.get_by_correo(form.correo.data)

        # Vemos si existe un administrativo con ese correo y si coincide la contraseña
        if administrativo is not None and administrativo.check_password(
            form.password.data
        ):
            # Si todo es correcto autenticamos al administrativo con 'login_user()' de Flask-login
            login_user(administrativo, remember=form.recuerdame.data)

            # Si recibimos el parámetro 'next' el usuario intenta acceder a una vista protegida
            next_page = request.args.get("next")
            if not next_page or url_parse(next_page).netloc != "":
                next_page = url_for("main.index")
            # Eliminamos mensaje flash ya que recoge un mensaje de error de acceso de la sesión anterior
            session.pop("_flashes", None)

            return redirect(next_page)
        else:
            error = "Correo o contraseña incorrectos"

    return render_template("auth/login_view.html", form=form, error=error)


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


# Hacemos el user_loader que no sirve nada más que para recoger la ID del usuario
# que está usando la aplicación
@login_manager.user_loader
def load_user(administrativo_id):
    return Administrativo.get_by_id(administrativo_id)
