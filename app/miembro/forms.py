from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length


class CreateMiembroForm(FlaskForm):
    dni = StringField("DNI", validators=[DataRequired(), Length(min=9, max=9)])
    nombre = StringField("Nombre", validators=[DataRequired()])
    apellidos = StringField("Apellidos", validators=[DataRequired()])
    correo = StringField("Correo", validators=[DataRequired(), Email()])
    telefono = IntegerField("Teléfono", validators=[DataRequired()])
    tipo = SelectField(
        "Tipo",
        choices=["Estudiante", "Profesor", "PAS", "Externo"],
        validators=[DataRequired()],
    )
    submit = SubmitField("Guardar")


class UpdateMiembroForm(FlaskForm):
    dni = StringField("DNI", render_kw={"readonly": True})
    nombre = StringField("Nombre", validators=[DataRequired()])
    apellidos = StringField("Apellidos", validators=[DataRequired()])
    correo = StringField("Correo", validators=[DataRequired(), Email()])
    telefono = IntegerField("Teléfono", validators=[DataRequired()])
    tipo = SelectField(
        "Tipo",
        choices=["Estudiante", "Profesor", "PAS", "Externo"],
        validators=[DataRequired()],
    )
    submit = SubmitField("Guardar")
