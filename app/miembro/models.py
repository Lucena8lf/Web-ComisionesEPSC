import datetime

from app import db

from sqlalchemy.orm import validates

from sqlalchemy import UniqueConstraint

import re

# print("importing models from", __name__)

# Cambiar de dni_miembro a id_miembro
miembros_comisiones = db.Table(
    "miembros_comisiones",
    db.Column("id_miembro", db.Integer, db.ForeignKey("miembro.id"), primary_key=True),
    db.Column(
        "id_comision", db.Integer, db.ForeignKey("comision.id"), primary_key=True
    ),
    db.Column(
        "fecha_incorporacion",
        db.DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
    ),
    db.Column("fecha_baja", db.DateTime, nullable=True),
)


class Miembro(db.Model):
    __tablename__ = "miembro"

    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.String(20), nullable=False)
    nombre = db.Column(db.String(80), nullable=False)
    apellidos = db.Column(db.String(128), nullable=False)
    correo = db.Column(db.String(256), unique=True, nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    tipo = db.Column(
        db.Enum("Estudiante", "Profesor", "PAS", "Externo"), nullable=False
    )
    activo = db.Column(db.Boolean, default=True)
    comisiones = db.relationship(
        "Comision",
        secondary=miembros_comisiones,
        back_populates="miembros",
    )
    # La opción secondary indica la tabla de relación que se utilizará para establecer la relación.
    # La opción backref agrega una propiedad "miembros" en la clase "Comision" que te
    # permite acceder a los objetos "Miembro" asociados a la comisión.
    informes = db.relationship(
        "Informe", backref="miembros", lazy=True, cascade="all, delete"
    )

    # Restricción para asegurar que es un teléfono válido de 9 dígitos
    __table_args__ = (
        db.CheckConstraint("length(telefono) == 9", name="check_telefono_length"),
        UniqueConstraint("dni", name="uq_dni"),
    )

    @validates("dni")
    def validate_dni(self, key, value):
        if not value:
            raise ValueError("El DNI es requerido.")
        if not re.match(r"^\d{8}[a-zA-Z]$", value):
            raise ValueError("El DNI debe ser un número seguido de una letra.")
        return value

    def __repr__(self):
        """
        Sobrecargamos el método __repr__ para representar como queramos los objetos
        de esta clase
        """
        return f"<Miembro {Miembro.correo}>"

    # Algunos métodos que nos serán útiles a la hora de trabajar con la clase
    def save(self):
        """
        Método para crear un nuevo miembro
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        """
        Método para obtener un miembro a partir de su id
        """
        return Miembro.query.get(id)

    @staticmethod
    def get_by_dni(dni):
        """
        Método para obtener un miembro a partir de su dni
        """
        return Miembro.query.filter_by(dni=dni).first()
