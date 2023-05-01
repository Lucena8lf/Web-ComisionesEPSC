# Fichero en el que se definen las rutas relacionadas con los miembros
from flask import render_template, request, url_for, redirect, flash, jsonify
from werkzeug.urls import url_parse

from flask_login import login_required, current_user

from . import miembro_bp

from .models import Miembro
from .forms import CreateMiembroForm, UpdateMiembroForm

from app import db

from sqlalchemy.exc import IntegrityError


# El decorador route se coge de los objetos blueprints
@miembro_bp.route("/miembros")
@login_required
def get_miembros():
    miembros = Miembro.query.all()
    return render_template("miembro/miembros_view.html", miembros=miembros)


@miembro_bp.route("/miembros/crear", methods=["GET", "POST"])
@login_required
def create_miembro():
    form = CreateMiembroForm()
    error = None
    dni_error = None
    telefono_error = None
    if form.validate_on_submit():
        dni = form.dni.data
        nombre = form.nombre.data
        apellidos = form.apellidos.data
        correo = form.correo.data
        telefono = form.telefono.data
        tipo = form.tipo.data

        # Comprobamos que no haya un miembro con el mismo dni y que es válido
        miembro = Miembro.get_by_dni(dni)
        if miembro is not None:
            # flash(f"El dni {dni} ya está siendo utilizado por otro miembro", error)
            dni_error = f"El dni {dni} ya está siendo utilizado por otro miembro"
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
                    flash("Miembro creado con éxito!", "success")
                    next_page = url_for("main.index")
                return redirect(next_page)
            except ValueError as e:
                # flash(str(e), "error")
                dni_error = str(e)
            except IntegrityError as e:
                db.session.rollback()
                if "check_telefono_length" in str(e):
                    telefono_error = "El número de teléfono debe tener 9 dígitos."
                else:
                    error = "Ha ocurrido un error al actualizar el miembro."
                    flash(error, "error")

    return render_template(
        "miembro/crearMiembro_view.html",
        form=form,
        error=error,
        dni_error=dni_error,
        telefono_error=telefono_error,
    )


@miembro_bp.route("/miembros/<int:miembro_id>/activar", methods=["POST"])
@login_required
def activate_miembro(miembro_id):
    # miembro = Miembro.query.get_or_404(miembro_id)
    miembro = Miembro.get_by_id(miembro_id)
    miembro.activo = True
    db.session.commit()
    # flash("Miembro activado!")
    return jsonify({"mensaje": f"Miembro {miembro_id} activado"}), 200


@miembro_bp.route("/miembros/<int:miembro_id>/desactivar", methods=["POST"])
@login_required
def deactivate_miembro(miembro_id):
    miembro = Miembro.get_by_id(miembro_id)
    miembro.activo = False
    db.session.commit()
    # flash("Miembro desactivado!")
    return jsonify({"mensaje": f"Miembro {miembro_id} desactivado"}), 200


@miembro_bp.route("/miembros/<int:miembro_id>", methods=["GET"])
@login_required
def consult_miembro(miembro_id):
    # Obtenemos el miembro por su id
    miembro = Miembro.get_by_id(miembro_id)
    return render_template("miembro/miembroInformation_view.html", miembro=miembro)
    # return render_template("miembro/updateMiembro_view.html", miembro=miembro)


@miembro_bp.route("/miembros/<int:miembro_id>/edit", methods=["GET", "POST"])
@login_required
def update_miembro(miembro_id):
    miembro = Miembro.get_by_id(miembro_id)
    form = UpdateMiembroForm(obj=miembro)
    error = None
    if form.validate_on_submit():
        # Recuperamos los datos que ya tiene
        form.populate_obj(miembro)

        try:
            db.session.commit()
            flash("Los datos del miembro se han actualizado correctamente.", "success")
            return redirect(url_for("miembro.consult_miembro", miembro_id=miembro.id))
        except IntegrityError as e:
            db.session.rollback()
            if "check_telefono_length" in str(e):
                error = "El número de teléfono debe tener 9 dígitos."
            else:
                error = "Ha ocurrido un error al actualizar el miembro."
                flash(error, "error")
    return render_template(
        "miembro/updateMiembro_view.html", form=form, miembro=miembro, error=error
    )
