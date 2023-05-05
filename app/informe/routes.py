from flask import (
    render_template,
    request,
    redirect,
    url_for,
    make_response,
)
from werkzeug.urls import url_parse

from flask_login import login_required

from sqlalchemy import select

from . import informe_bp

from .models import Informe
from app.miembro.models import Miembro, miembros_comisiones
from app.comision.models import Comision

from .forms import CreateInformeForm

from app import db

from pdfkit import from_string

import datetime


@informe_bp.route("/informes", methods=["GET", "POST"])
@login_required
def generate_informe():
    form = CreateInformeForm()

    # Las opciones del select serán todos los miembros ya estén activos o no
    # Le pasamos una tupla donde el valor será la ID del miembro y la etiqueta su nombre y apellidos
    miembros = [(m.id, m.nombre, m.apellidos) for m in Miembro.query.all()]
    miembros = [(m[0], m[1] + " " + m[2]) for m in miembros]
    form.miembro.choices = miembros
    if request.method == "POST" and form.validate_on_submit():
        secretario = form.secretario.data
        fecha_inicio = form.fecha_inicio.data
        fecha_fin = form.fecha_fin.data
        tipo_informe = form.tipo_informe.data  # 'escuela' o 'comision'
        miembro = form.miembro.data  # ID_Miembro

        # Creamos el informe y lo guardamos
        informe = Informe(
            secretario=secretario,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tipo=tipo_informe,
            id_miembro=miembro,
        )

        informe.save()

        # Abrimos una nueva pestaña en la que el usuario verá el PDF generado para el miembro elegido
        # Comprobamos si se ha pasado por la URL el parámetro next
        next_page = request.args.get("next", None)
        if not next_page or url_parse(next_page).netloc != "":
            if tipo_informe == "comision":
                next_page = url_for(
                    "informe.informe_comisiones",
                    secretario=secretario,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    id_miembro=miembro,
                )
            elif tipo_informe == "escuela":
                next_page = url_for(
                    "informe.informe_escuela",
                    secretario=secretario,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    id_miembro=miembro,
                )
        return redirect(next_page)

    return render_template("informe/generateInforme_view.html", form=form)


@informe_bp.route(
    "/informe/comisiones/<secretario>/<fecha_inicio>/<fecha_fin>/<int:id_miembro>"
)
@login_required
def informe_comisiones(secretario, fecha_inicio, fecha_fin, id_miembro):
    # Aquí hacemos todo lo del HTML
    # A partir de la ID del miembro recuperamos todos sus datos y las comisiones a las
    # que ha perteneceido durante todo ese tiempo
    miembro = Miembro.get_by_id(id_miembro)  # Aquí ya tenemos todos sus datos

    # Ahora recuperamos todas las comisiones a las que ha pertenecido durante todo ese tiempo
    # Usamos 'select' de SQLAlchemy aquí para mejorar la claridad de la setencia
    comisiones = db.session.execute(
        select(
            miembros_comisiones.columns.id_comision,
            miembros_comisiones.columns.fecha_incorporacion,
            miembros_comisiones.columns.fecha_baja,
        ).where(
            miembros_comisiones.columns.id_miembro == id_miembro,
            miembros_comisiones.columns.fecha_incorporacion.between(
                fecha_inicio, fecha_fin
            ),
        )
    ).fetchall()

    # Obtenemos el nombre de esas comisiones a partir de la ID
    # Primero obtenemos todas las ID de las comisiones de la lista anterior
    id_comisiones = [c[0] for c in comisiones]
    # Ahora recuperamos los nombres
    nombres_comisiones = (
        db.session.query(Comision.id, Comision.nombre)
        .filter(Comision.id.in_(id_comisiones))
        .all()
    )
    # Creamos una lista de tuplas con las comisiones, fechas y nombres utilizando map() para agregar el nombre de la comisión
    comisiones_con_nombre = list(
        map(
            lambda c: (
                c[0],
                c[1],
                c[2],
                next((n[1] for n in nombres_comisiones if n[0] == c[0]), ""),
            ),
            comisiones,
        )
    )

    # Ordenamos la lista de manera ascendente en función de la fecha de inicio
    comisiones_con_nombre = sorted(comisiones_con_nombre, key=lambda tupla: tupla[1])

    # Borramos la comisión 'Junta de Escuela' si existe ya que no pertenece a este informe
    for tupla in comisiones_con_nombre:
        if tupla[3] == "Junta de Escuela":
            comisiones_con_nombre.remove(tupla)
            break

    # Obtenemos el HTML
    html = render_template(
        "informe/blueprintComisiones_view.html",
        secretario=secretario,
        miembro=miembro,
        comisiones=comisiones_con_nombre,
        fecha_actual=datetime.datetime.now(),
    )

    # PDF options
    options = {
        "page-size": "A4",
        "margin-top": "1.0cm",
        "margin-right": "1.0cm",
        "margin-bottom": "1.0cm",
        "margin-left": "1.0cm",
        "encoding": "UTF-8",
        "enable-local-file-access": "",
    }

    # Construimos el PDF a partir del HTML
    pdf = from_string(html, options=options)

    # Descargamos el PDF
    # return Response(pdf, mimetype="application/pdf")
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=certificado.pdf"
    return response


@informe_bp.route(
    "/informe/escuela/<secretario>/<fecha_inicio>/<fecha_fin>/<int:id_miembro>"
)
@login_required
def informe_escuela(secretario, fecha_inicio, fecha_fin, id_miembro):
    miembro = Miembro.get_by_id(id_miembro)

    # Aquí sólo nos importa la comisión "Junta de Escuela"
    # Recuperamos el ID de esta comisión
    id_comision = Comision.query.filter_by(nombre="Junta de Escuela").first().id

    if not id_comision:
        return "Parece que la comisión 'Junta de Escuela' no se encuentra"
    # Si este miembro está en esa comsión recuperamos sus fechas de incorporación y de baja
    comision = db.session.execute(
        select(
            miembros_comisiones.columns.fecha_incorporacion,
            miembros_comisiones.columns.fecha_baja,
        ).where(
            miembros_comisiones.columns.id_miembro == id_miembro,
            miembros_comisiones.columns.id_comision == id_comision,
            miembros_comisiones.columns.fecha_incorporacion.between(
                fecha_inicio, fecha_fin
            ),
        )
    ).first()

    if not comision:
        return "Parece que este miembro no pertenece ni ha pertenecido nunca a 'Junta de Escuela'"

    # Obtenemos el HTML
    html = render_template(
        "informe/blueprintEscuela_view.html",
        secretario=secretario,
        miembro=miembro,
        comision=comision,
        fecha_actual=datetime.datetime.now(),
    )

    # PDF options
    options = {
        "page-size": "A4",
        "margin-top": "1.0cm",
        "margin-right": "1.0cm",
        "margin-bottom": "1.0cm",
        "margin-left": "1.0cm",
        "encoding": "UTF-8",
        "enable-local-file-access": "",
    }

    # Construimos el PDF a partir del HTML
    pdf = from_string(html, options=options)

    # Descargamos el PDF
    # return Response(pdf, mimetype="application/pdf")
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=certificado.pdf"
    return response
