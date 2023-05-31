from flask import (
    render_template,
    url_for,
    request,
    redirect,
    flash,
    current_app,
)
from werkzeug.urls import url_parse

from flask_login import login_required, current_user

from . import comision_bp

from .models import Comision
from app.miembro.models import Miembro, miembros_comisiones

from .forms import CreateComisionForm, CloseComisionForm, UpdateClosedComisionForm

from app import db

from unidecode import unidecode


@comision_bp.route("/comisiones")
@login_required
def get_comisiones():
    # comisiones = Comision.query.all()
    # return render_template("comision/comisiones_view.html", comisiones=comisiones)
    page = int(request.args.get("page", 1))
    per_page = current_app.config["COMISIONES_PER_PAGE"]
    comisiones_pagination = Comision.get_all_paginated(page, per_page)
    return render_template(
        "comision/comisiones_view.html", comisiones_pagination=comisiones_pagination
    )


@comision_bp.route("/comisiones/crear", methods=["GET", "POST"])
@login_required
def create_comision():
    form = CreateComisionForm()
    error = None

    # Para el campo "miembros" solo se podrán seleccionar miembros que estén activos
    miembros_activos = [
        (m.id, m.nombre, m.apellidos)
        for m in Miembro.query.filter_by(activo=True).all()
    ]

    # Añadimos una opción vacía al principio de la lista por si no quiere seleccionar ninguno
    miembros_activos.insert(0, ("", "Seleccione un miembro"))

    # Ahora para el select no utilizamos flask-wtforms por lo que lo pasamos al render_template
    # form.miembros.choices = miembros_activos

    if request.method == "POST" and form.validate_on_submit():
        nombre = form.nombre.data
        comentarios = form.comentarios.data
        fecha_apertura = form.fecha_apertura.data
        id_miembros = request.form.getlist("miembros")
        cargos = request.form.getlist("cargos")
        print("Cargos -> ", cargos)

        # Si ha seleccionado uno o más miembros...

        # Comprobamos que no haya una comisión con el mismo nombre exacto
        comision = Comision.get_by_nombre(nombre)

        if comision is not None:
            flash(f"El nombre {nombre} ya está siendo utilizado por otra comisión")
        else:
            # Creamos la comisión
            comision = Comision(
                nombre=nombre,
                comentarios=comentarios,
                fecha_apertura=fecha_apertura,
                fecha_cierre=None,
            )

            # Si no ha seleccionado ningún miembro y crea la comisión vacía...
            if id_miembros[0] == "":
                # No tiene miembros, por lo que la lista pasada será vacía (está por defecto)
                comision.save()
            else:
                # Se ha introducido al menos la id de un miembro
                # Ej: ['1', ''] o ['1', '2']
                # Asignamos a la lista de los id de los miembros el cargo correspondiente si se le ha asignado
                id_cargos_miembros = list(zip(id_miembros, cargos))
                comision.save(miembros=id_cargos_miembros)

            # Comprobamos si se ha pasado por la URL el parámetro next
            next_page = request.args.get("next", None)
            if not next_page or url_parse(next_page).netloc != "":
                flash("¡Comisión creada con éxito!", "success")
                next_page = url_for("main.index")
            return redirect(next_page)
    return render_template(
        "comision/crearComision_view.html",
        miembros=miembros_activos,
        form=form,
        error=error,
    )


@comision_bp.route("/comisiones/<int:id_comision>/cerrar", methods=["GET", "POST"])
@login_required
def cerrar_comision(id_comision):
    comision = Comision.get_by_id(id_comision)

    # Muestra un formulario de dos campos
    #   1. El nombre de la comisión debe coincidir
    #   2. Debe introducir una fecha de cierre válida, es decir, posterior a la de apertura
    form = CloseComisionForm()

    # Ponemos por defecto el nombre de esa comisión en el campo del nombre
    form.nombre.data = comision.nombre

    if request.method == "POST" and form.validate_on_submit():
        nombre = form.nombre.data
        fecha_cierre = form.fecha_cierre.data

        # Comprobamos que el nombre introducido sea correcto
        # Es decir, que sea igual que el de la ID que tenemos
        comision_real = Comision.get_by_id(id_comision)
        comision_introducida = Comision.get_by_nombre(nombre)
        # Al comparar los nombres aplicamos case insensitive y eliminamos los acentos
        # para permitir al usuario una comparación más flexible
        if unidecode(comision_real.nombre.lower()) != unidecode(nombre.lower()):
            flash(
                "El nombre introducido no se corresponde con la comisión que se desea cerrar. Por favor, vuelva a comprobar la comisión.",
                "error",
            )
        elif comision_real.fecha_apertura >= fecha_cierre:
            flash(
                "La fecha de cierre debe ser posterior a la fecha de apertura de la comisión.",
                "error",
            )
        else:
            # La comisión es correcta

            # Al método debemos pasarle tanto la fecha de cierre como la lista de miembros
            # que pertencen a esa comisión (nos devuelve sus IDs)
            # Podemos tener miembros repetidos ya que un miembro puedo incorporarse varias
            # veces a una misma comisión, por lo que usamos .distinct()
            miembros_comision = [
                miembro.id_miembro
                for miembro in db.session.query(miembros_comisiones.c.id_miembro)
                .filter_by(id_comision=id_comision)
                .distinct()
                .all()
            ]

            comision.close(fecha_cierre, miembros_comision)

            # Comprobamos si se ha pasado por la URL el parámetro next
            next_page = request.args.get("next", None)
            if not next_page or url_parse(next_page).netloc != "":
                flash("¡Comisión cerrada con éxito!", "success")
                next_page = url_for("main.index")
            return redirect(next_page)

    return render_template("comision/cerrarComision_view.html", form=form)


@comision_bp.route("/comisiones/<int:id_comision>", methods=["GET"])
@login_required
def consult_comision(id_comision):
    # A la vista le pasamos tanto la comisión como una lista con todos los miembros
    # de esa comisión (la lista contendrá los IDs de cada miembro)
    comision = Comision.get_by_id(id_comision)

    # Con 'miembro.id_miembro' le decimos que recorra todos los resultados de la
    # consulta de abajo y extraiga el valor de la columna 'id_miembro'
    data_miembros_comision = [
        (
            miembro.id_miembro,
            miembro.fecha_incorporacion,
            miembro.fecha_baja,
            miembro.cargo,
            miembro.motivo_baja,
        )
        for miembro in db.session.query(
            miembros_comisiones.c.id_miembro,
            miembros_comisiones.c.fecha_incorporacion,
            miembros_comisiones.c.fecha_baja,
            miembros_comisiones.c.cargo,
            miembros_comisiones.c.motivo_baja,
        )
        .filter_by(id_comision=id_comision)
        .all()
    ]

    # A partir de esta lista (ID, fecha_incorporacion, fecha_baja, cargo, motivo_baja) que está ordenada en el orden
    # en el que el usuario ha ido incorporando miembros a la comisión.

    # Creamos un diccionario para asociar la ID de cada miembro a su nombre completo. Así uniremos
    # el nombre completo de cada miembro a la lista anterior de tuplas usando diccionarios
    # para relacionar la información -> (ID_listaTuplas -> ID_nombreCompleto)
    # creamos el diccionario "nombres_completos"
    nombres_completos = {}
    for miembro in Miembro.query.all():
        id_miembro = miembro.id
        nombre_completo = miembro.nombre + " " + miembro.apellidos
        nombres_completos[id_miembro] = nombre_completo

    # Suponiendo que data_miembros_comision es una lista de tuplas donde cada tupla tiene 5 elementos: ID, fecha_incorporación, fecha_baja, cargo, motivo_baja
    for i in range(len(data_miembros_comision)):
        id_miembro = data_miembros_comision[i][0]
        nombre_completo = nombres_completos.get(id_miembro, "")
        data_miembros_comision[i] = data_miembros_comision[i] + (nombre_completo,)

    # print("Nombres_completos -> ", nombres_completos)
    # print("Data_miembros_comision -> ", data_miembros_comision)

    return render_template(
        "comision/comisionInformation_view.html",
        comision=comision,
        data_miembros_comision=data_miembros_comision,
    )


@comision_bp.route("/comisiones/<int:id_comision>/edit", methods=["GET", "POST"])
@login_required
def update_comision(id_comision):
    """
    Ruta para actualizar los datos de una comisión que no ha sido cerrada
        :param id_comision: ID de la comisión que se desea actualizar
    """
    comision = Comision.get_by_id(id_comision)
    form = CreateComisionForm(obj=comision)

    # Obtenemos la lista de miembros que pertenecen a esta comisión
    # --- #
    # (Código repetido)
    data_miembros_comision = [
        (
            miembro.id,
            miembro.id_miembro,
            miembro.fecha_incorporacion,
            miembro.fecha_baja,
            miembro.cargo,
            miembro.motivo_baja,
        )
        for miembro in db.session.query(
            miembros_comisiones.c.id,
            miembros_comisiones.c.id_miembro,
            miembros_comisiones.c.fecha_incorporacion,
            miembros_comisiones.c.fecha_baja,
            miembros_comisiones.c.cargo,
            miembros_comisiones.c.motivo_baja,
        )
        .filter_by(id_comision=id_comision)
        .all()
    ]

    nombres_completos = {}
    for miembro in Miembro.query.all():
        id_miembro = miembro.id
        nombre_completo = miembro.nombre + " " + miembro.apellidos
        nombres_completos[id_miembro] = nombre_completo

    # Suponiendo que data_miembros_comision es una lista de tuplas donde cada tupla tiene 6 elementos:
    # (ID, id_miembro, fecha_incorporación, fecha_baja, cargo, motivo_baja)
    for i in range(len(data_miembros_comision)):
        id_miembro = data_miembros_comision[i][1]
        nombre_completo = nombres_completos.get(id_miembro, "")
        data_miembros_comision[i] = data_miembros_comision[i] + (nombre_completo,)

    # --- #
    print("data miembros comision -> ", data_miembros_comision)

    # Obtenemos todos los miembros activos que son los que se pueden añadir a la comisión
    # A diferencia de crear la comisión, ahora sólo obtenemos los miembros activos
    # que NO formen parte de esa comisión y NO tengan una fecha de baja
    # Si alguno fue añadido pero ya tiene fecha de baja se puede añadir otra vez
    id_miembros_comision = [
        miembro[1] for miembro in data_miembros_comision if miembro[3] is None
    ]  # Estos son los miembros de la comisión que no se pueden volver a añadir ya que no tienen una fecha de baja
    miembros_activos = [
        (m.id, m.nombre, m.apellidos)
        for m in Miembro.query.filter_by(activo=True)
        .filter(Miembro.id.not_in(id_miembros_comision))
        .all()
    ]
    # 'miembros_activos' -> miembros que se pueden añadir a la comisión

    # Añadimos una opción vacía al principio de la lista por si no quiere seleccionar ninguno
    miembros_activos.insert(0, ("", "Seleccione un miembro"))

    error_message = None
    error_name_message = None
    # Usamos populate_obj pero esto solo actualiza los campos que tiene el wtform,
    # nos lo que manejamos aparte como son los select
    if request.method == "POST" and form.validate_on_submit:
        # Manejo de errores al introducir datos (fecha_baja > fecha_incorporacion, nombre repetido, etc.)
        # ...
        # Comprobamos que no haya introducido una comisión con un nombre ya existente
        new_nombre = form.nombre.data
        new_comentarios = form.comentarios.data
        new_fecha_apertura = form.fecha_apertura.data
        if (
            Comision.get_by_nombre(new_nombre) is not None
            and new_nombre != comision.nombre
        ):
            error_name_message = f"El nombre '{new_nombre}' está siendo actualmente utilizado por otra comisión. Por favor, elige otro nombre."

        # Ahora debemos actualizar los campos que NO controla wtforms
        #
        # --- Actualización de miembros existentes ---
        #
        # Por un lado debemos comprobar si a algún miembro que ya había en esa comisión
        # se le ha cambiado su fecha de incorporación o de baja

        # 1. Recuperamos todas las fechas de incorporación que han sido introducidas
        # Cada fecha de incorporación la asociaremos con la correspondiente ID de la tupla
        fechas_incorporacion = []
        for key in request.form:
            if "fecha_incorporacion_modificada-" in key:
                # Obtenemos ID de la tupla desde el nombre del campo
                id_tupla = key.split("-")[-1]

                # Obtenemos la fecha de incorporación
                fecha_incorporacion = request.form[key]

                # Sólo la añadimos a la lista si no es una cadena vacía
                if fecha_incorporacion != "":
                    fechas_incorporacion.append(
                        (id_tupla, fecha_incorporacion)
                    )  # Añadimos tupla a la lista

        # 2. Recuperamos todas las fechas de baja que han sido introducidas
        # Cada fecha de baja la asociaremos con la correspondiente ID de la tupla
        fechas_baja = []
        for key in request.form:
            if "fecha_baja_modificada-" in key:
                # Obtenemos ID del miembro desde el nombre del campo
                id_tupla = key.split("-")[-1]
                # Obtenemos la fecha de baja
                fecha_baja = request.form[key]

                # Sólo la añadimos a la lista si no es una cadena vacía
                if fecha_baja != "":
                    fechas_baja.append(
                        (id_tupla, fecha_baja)
                    )  # Añadimos tupla a la lista

        # 3. Recuperamos todos los cargos que han sido introducidos para los miembros existentes
        cargos = []
        for key in request.form:
            if "cargo_modificado-" in key:
                id_tupla = key.split("-")[-1]
                cargo = request.form[key]

                if cargo != "":
                    cargos.append((id_tupla, cargo))
                else:
                    cargos.append((id_tupla, None))

        # 4. Recuperamos tods los motivos de baja que han sido introducidos para los miembros existentes
        motivos_baja = []
        for key in request.form:
            if "motivo_baja_modificado-" in key:
                id_tupla = key.split("-")[-1]
                motivo_baja = request.form[key]

                if motivo_baja != "":
                    motivos_baja.append((id_tupla, motivo_baja))
                else:
                    motivos_baja.append((id_tupla, None))
                # Con las fechas de baja podríamos hacer lo mismo???

        # POR AQUI...
        # --- Nuevos miembros ---
        #
        # Por otro lado, comprobamos si se ha añadido un nuevo miembro a esa comisión el
        # cual no estaba antes
        miembros_nuevos_id = request.form.getlist("miembros")

        # Al añadirse un nuevo miembro:
        #   - fecha_incorporacion: Obligatorio
        #   - fecha_baja: Opcional (si no se introduce == None)
        #   - cargo: Opcional (si no se introduce == None)
        #   - motivo_baja: Opcional (si no se introduce == None)
        # Por lo que al método de la base de datos le pasaremos una lista que esté formada
        # por tuplas de 3 elementos (id_nuevo_miembro, fecha_incorporacion, fecha_baja, cargo, motivo_baja)
        # Primero obtenemos estos parámetros
        fechas_incorporacion_nuevo_miembro = request.form.getlist(
            "fecha_incorporacion_nuevo_miembro"
        )
        fechas_baja_nuevo_miembro = request.form.getlist("fecha_baja_nuevo_miembro")
        cargos_nuevo_miembro = request.form.getlist("cargo_nuevo_miembro")
        motivos_baja_nuevo_miembro = request.form.getlist("motivo_baja_nuevo_miembro")

        # Asociamos todas las fechas a sus respectivos miembros
        miembros_nuevos = list(
            zip(
                miembros_nuevos_id,
                fechas_incorporacion_nuevo_miembro,
                fechas_baja_nuevo_miembro,
                cargos_nuevo_miembro,
                motivos_baja_nuevo_miembro,
            )
        )

        # print("Lista fechas de incorporación -> ", fechas_incorporacion)
        # print("Lista fechas de baja -> ", fechas_baja)
        print("Lista miembros nuevos -> ", miembros_nuevos)
        # return render_template(
        #    "comision/updateComision_view.html",
        #    form=form,
        #    comision=comision,
        #    miembros=miembros_activos,
        #    miembros_comision=miembros_comision,
        # )

        # 'fechas_incorporacion' nunca puede estar vacío ya que un miembro siempre tendrá una fecha de
        # incorporación. Las fechas de baja y los miembros nuevos si pueden ser vacíos
        # (A menos que la comisión esté vacía???)
        #
        # Siempre vamos a pasar las listas de cargos modificados y motivos de baja modificados
        if not fechas_baja and miembros_nuevos[0][0] == "":
            # Sólo se ha modificado la fecha de incorporación de un miembro existente
            error_message = comision.update(
                fechas_incorporacion_nuevas=fechas_incorporacion,
                cargos_nuevos=cargos,
                motivos_baja_nuevos=motivos_baja,
            )
            if error_message:
                flash(error_message, "error")
        elif fechas_baja and miembros_nuevos[0][0] == "":
            # Se ha dado de baja a un miembro existente pero no se ha añadido ningún
            # miembro. (También se actualiza por si acaso las fechas de incorporación)
            error_message = comision.update(
                fechas_incorporacion_nuevas=fechas_incorporacion,
                fechas_baja_nuevas=fechas_baja,
                cargos_nuevos=cargos,
                motivos_baja_nuevos=motivos_baja,
            )
            if error_message:
                flash(error_message, "error")
        elif not fechas_baja and miembros_nuevos[0][0] != "":
            # NO se ha dado de baja a ningún miembro existente pero se ha añadido algún
            # miembro nuevo (También se actualiza por si acaso las fechas de incorporación)
            error_message = comision.update(
                fechas_incorporacion_nuevas=fechas_incorporacion,
                cargos_nuevos=cargos,
                motivos_baja_nuevos=motivos_baja,
                miembros_nuevos=miembros_nuevos,
            )
            if error_message:
                flash(error_message, "error")
        else:
            # Se han hecho ambas cosas
            error_message = comision.update(
                fechas_incorporacion_nuevas=fechas_incorporacion,
                fechas_baja_nuevas=fechas_baja,
                cargos_nuevos=cargos,
                motivos_baja_nuevos=motivos_baja,
                miembros_nuevos=miembros_nuevos,
            )
            if error_message:
                flash(error_message, "error")

        if error_name_message:
            flash(error_name_message, "error")
        elif not error_name_message and not error_message:
            # Si ha cambiado la fecha de apertura comprobamos que todos los miembros que tengan
            # su fecha de incorporación ANTERIOR a esta fecha de apertura, se establezca por defecto
            # que tenga como fecha de incorporación la fecha de apertura de la comisión
            if new_fecha_apertura != comision.fecha_apertura:
                comision.check_new_fecha_apertura(new_fecha_apertura)

            # Actualizamos los campos que soporta wtforms (nombre, comentarios, fecha_apertura)
            form.populate_obj(comision)
            db.session.commit()
            flash(
                "Los datos de la comisión se han actualizado correctamente.", "success"
            )
        return redirect(url_for("comision.consult_comision", id_comision=comision.id))

    # print("Data_miembros ->", data_miembros_comision)
    return render_template(
        "comision/updateComision_view.html",
        form=form,
        comision=comision,
        miembros=miembros_activos,
        miembros_comision=data_miembros_comision,
    )


@comision_bp.route("/comisiones/<int:id_comision>/edit-close", methods=["GET", "POST"])
@login_required
def update_comision_cerrada(id_comision):
    """
    Ruta para actualizar los datos de una comisión que ya ha sido cerrada
        :param id_comision: ID de la comisión que se desea actualizar
    """
    comision = Comision.get_by_id(id_comision)
    form = UpdateClosedComisionForm(obj=comision)

    # Obtenemos la lista de miembros que pertenecen a esta comisión
    # --- #
    # (Código repetido)
    data_miembros_comision = [
        (
            miembro.id,
            miembro.id_miembro,
            miembro.fecha_incorporacion,
            miembro.fecha_baja,
            miembro.cargo,
            miembro.motivo_baja,
        )
        for miembro in db.session.query(
            miembros_comisiones.c.id,
            miembros_comisiones.c.id_miembro,
            miembros_comisiones.c.fecha_incorporacion,
            miembros_comisiones.c.fecha_baja,
            miembros_comisiones.c.cargo,
            miembros_comisiones.c.motivo_baja,
        )
        .filter_by(id_comision=id_comision)
        .all()
    ]

    nombres_completos = {}
    for miembro in Miembro.query.all():
        id_miembro = miembro.id
        nombre_completo = miembro.nombre + " " + miembro.apellidos
        nombres_completos[id_miembro] = nombre_completo

    # Suponiendo que data_miembros_comision es una lista de tuplas donde cada tupla tiene 4 elementos: ID, id_miembro, fecha_incorporación, fecha_baja
    for i in range(len(data_miembros_comision)):
        id_miembro = data_miembros_comision[i][1]
        nombre_completo = nombres_completos.get(id_miembro, "")
        data_miembros_comision[i] = data_miembros_comision[i] + (nombre_completo,)

    # --- #

    error_name_message = None
    # Usamos populate_obj pero esto solo actualiza los campos que tiene el wtform,
    # nos lo que manejamos aparte como son los select
    if request.method == "POST" and form.validate_on_submit:
        # Comprobamos que no haya introducido una comisión con un nombre ya existente
        new_nombre = form.nombre.data
        if (
            Comision.get_by_nombre(new_nombre) is not None
            and new_nombre != comision.nombre
        ):
            error_name_message = f"El nombre '{new_nombre}' está siendo actualmente utilizado por otra comisión. Por favor, elige otro nombre."

        if error_name_message:
            flash(error_name_message, "error")
        else:
            # Actualizamos los campos
            form.populate_obj(comision)
            db.session.commit()
            flash(
                "Los datos de la comisión se han actualizado correctamente.", "success"
            )
        return redirect(url_for("comision.consult_comision", id_comision=comision.id))

    return render_template(
        "comision/updateComisionCerrada_view.html",
        form=form,
        comision=comision,
        miembros_comision=data_miembros_comision,
    )
