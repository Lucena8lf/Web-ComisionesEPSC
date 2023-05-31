from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, Optional

import datetime


class CreateComisionForm(FlaskForm):
    nombre = StringField("Nombre comisión", validators=[DataRequired()])
    comentarios = TextAreaField("Comentarios", validators=[Optional()])
    fecha_apertura = DateField("Fecha de apertura", default=datetime.datetime.utcnow)

    submit = SubmitField("Guardar")


class CloseComisionForm(FlaskForm):
    nombre = StringField("Nombre comisión", validators=[DataRequired()])
    fecha_cierre = DateField("Fecha de cierre", validators=[DataRequired()])

    submit = SubmitField("Cerrar comisión")


class UpdateClosedComisionForm(FlaskForm):
    nombre = StringField("Nombre comisión", validators=[DataRequired()])
    comentarios = TextAreaField("Comentarios", validators=[Optional()])

    submit = SubmitField("Guardar")
