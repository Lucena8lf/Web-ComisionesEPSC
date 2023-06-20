from flask import (
    render_template,
    request,
    url_for,
    redirect,
    flash,
    jsonify,
    current_app,
)
from werkzeug.urls import url_parse

from flask_login import login_required, current_user

from . import miembro_bp

from .models import Miembro
from .forms import CreateMiembroForm, UpdateMiembroForm

from app import db

from sqlalchemy.exc import IntegrityError

from sqlalchemy import func


@miembro_bp.route("/miembros")
@login_required
def get_miembros():
    """
    Ruta para obtener todos los miembros
    """
    page = int(request.args.get("page", 1))
    per_page = current_app.config["MIEMBROS_PER_PAGE"]
    miembros_pagination = Miembro.get_all_paginated(page, per_page)
    return render_template(
        "miembro/miembros_view.html", miembros_pagination=miembros_pagination
    )


@miembro_bp.route("/miembros/crear", methods=["GET", "POST"])
@login_required
def create_miembro():
    """
    Ruta para crear un nuevo miembro
    """
    form = CreateMiembroForm()
    error = None
    dni_error = None
    telefono_error = None
    correo_error = None
    if form.validate_on_submit():
        dni = form.dni.data
        nombre = form.nombre.data
        apellidos = form.apellidos.data
        correo = form.correo.data or None
        telefono = form.telefono.data or None
        tipo = form.tipo.data

        # Comprobamos que no haya un miembro con el mismo dni y que es válido
        miembro = Miembro.get_by_dni(dni)
        if miembro is not None:
            dni_error = "El dni introducido ya está siendo utilizado por otro miembro"
        else:
            # Comprobamos que no haya un miembro con el mismo correo
            miembro_correo = Miembro.query.filter(
                func.lower(Miembro.correo) == func.lower(correo)
            ).first()
            if miembro_correo is not None and correo != "":
                correo_error = (
                    "El correo introducido ya está siendo utilizado por otro miembro"
                )
            else:
                try:
                    # Creamos el miembro y lo guardamos
                    miembro = Miembro(
                        dni=dni,
                        nombre=nombre,
                        apellidos=apellidos,
                        correo=correo,
                        telefono=telefono,
                        tipo=tipo,
                    )
                    miembro.save()

                    # Comprobamos si se ha pasado por la URL el parámetro next
                    next_page = request.args.get("next", None)
                    if not next_page or url_parse(next_page).netloc != "":
                        flash("¡Miembro creado con éxito!", "success")
                        next_page = url_for("main.index")
                    return redirect(next_page)
                except ValueError as e:
                    dni_error = str(e)
                except IntegrityError as e:
                    db.session.rollback()
                    if "check_telefono_length" in str(e):
                        telefono_error = "El número de teléfono debe tener 9 dígitos."
                    else:
                        error = "Ha ocurrido un error al crear el miembro."
                        flash(error, "error")

    return render_template(
        "miembro/crearMiembro_view.html",
        form=form,
        error=error,
        dni_error=dni_error,
        telefono_error=telefono_error,
        correo_error=correo_error,
    )


@miembro_bp.route("/miembros/<int:miembro_id>/activar", methods=["POST"])
@login_required
def activate_miembro(miembro_id):
    """
    Ruta para activar un miembro
        :param miembro_id: ID del miembro que se desea activar
    """
    miembro = Miembro.get_by_id(miembro_id)
    miembro.activo = True
    db.session.commit()
    return jsonify({"mensaje": f"Miembro {miembro_id} activado"}), 200


@miembro_bp.route("/miembros/<int:miembro_id>/desactivar", methods=["POST"])
@login_required
def deactivate_miembro(miembro_id):
    """
    Ruta para desactivar un miembro
        :param miembro_id: ID del miembro que se desea desactivar
    """
    miembro = Miembro.get_by_id(miembro_id)
    miembro.activo = False
    db.session.commit()
    return jsonify({"mensaje": f"Miembro {miembro_id} desactivado"}), 200


@miembro_bp.route("/miembros/<int:miembro_id>", methods=["GET"])
@login_required
def consult_miembro(miembro_id):
    """
    Ruta para consultar un miembro
        :param miembro_id: ID del miembro que se desea consultar
    """
    # Obtenemos el miembro por su id
    miembro = Miembro.get_by_id(miembro_id)
    return render_template("miembro/miembroInformation_view.html", miembro=miembro)


@miembro_bp.route("/miembros/<int:miembro_id>/edit", methods=["GET", "POST"])
@login_required
def update_miembro(miembro_id):
    """
    Ruta para actualizar los datos un miembro
        :param miembro_id: ID del miembro que se desea actualizar
    """
    miembro = Miembro.get_by_id(miembro_id)
    form = UpdateMiembroForm(obj=miembro)
    telefono_error = None
    correo_error = None
    if form.validate_on_submit():
        # Recuperamos los datos que ya tiene
        form.populate_obj(miembro)

        # Comprobamos que no haya otro miembro con el mismo correo
        correo_repetido = Miembro.query.filter(
            Miembro.id != miembro.id,
            (func.lower(Miembro.correo) == func.lower(miembro.correo)),
        ).first()

        if correo_repetido is not None and form.correo.data != "":
            correo_error = (
                "El correo introducido ya está siendo utilizado por otro miembro"
            )
        else:
            try:
                db.session.commit()
                flash(
                    "Los datos del miembro se han actualizado correctamente.", "success"
                )
                return redirect(
                    url_for("miembro.consult_miembro", miembro_id=miembro.id)
                )
            except IntegrityError as e:
                db.session.rollback()
                if "check_telefono_length" in str(e):
                    telefono_error = "El número de teléfono debe tener 9 dígitos."
                else:
                    telefono_error = "Ha ocurrido un error al actualizar el miembro."
                    flash(telefono_error, "error")
    return render_template(
        "miembro/updateMiembro_view.html",
        form=form,
        miembro=miembro,
        telefono_error=telefono_error,
        correo_error=correo_error,
    )
