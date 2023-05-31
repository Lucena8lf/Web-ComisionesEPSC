from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    SelectField,
    DateField,
    RadioField,
)
from wtforms.validators import DataRequired


class CreateInformeForm(FlaskForm):
    secretario = StringField("Secretario", validators=[DataRequired()])
    fecha_inicio = DateField("Fecha de inicio", validators=[DataRequired()])
    fecha_fin = DateField("Fecha de fin", validators=[DataRequired()])
    miembro = SelectField("Miembros", validators=[DataRequired()])
    tratamiento = StringField("Tratamiento", validators=[DataRequired()])
    tipo_informe = RadioField(
        "Tipo",
        choices=[
            ("comision", "Pertenencia Comisiones"),
            ("escuela", "Pertenencia Junta Escuela"),
        ],
        default="comision",
    )
    formato_informe = RadioField(
        "Formato",
        choices=[("pdf", "PDF"), ("docx", "DOCX")],
        default="pdf",
    )

    submit = SubmitField("Generar informe")
