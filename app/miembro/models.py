import datetime

from datetime import date

from app import db

from sqlalchemy.orm import validates

from sqlalchemy import UniqueConstraint

import re

miembros_comisiones = db.Table(
    "miembros_comisiones",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("id_miembro", db.Integer, db.ForeignKey("miembro.id"), nullable=False),
    db.Column("id_comision", db.Integer, db.ForeignKey("comision.id"), nullable=False),
    db.Column(
        "fecha_incorporacion",
        db.Date,
        nullable=False,
        default=date.today(),
    ),
    db.Column("fecha_baja", db.Date, nullable=True),
    db.Column("cargo", db.String(1000), nullable=True),
    db.Column("motivo_baja", db.String(1000), nullable=True),
)


class Miembro(db.Model):
    __tablename__ = "miembro"

    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.String(20), nullable=False)
    nombre = db.Column(db.String(80), nullable=False)
    apellidos = db.Column(db.String(128), nullable=False)
    correo = db.Column(db.String(256), nullable=True)
    telefono = db.Column(db.Integer, nullable=True)
    tipo = db.Column(db.Enum("Estudiante", "PDI", "PAS", "Externo"), nullable=False)
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

    @staticmethod
    def get_all_paginated(page=1, per_page=20):
        """
        Método que devuelve las miembros paginados
            :param page: Página a partir de la cual se obtienen los resultados
            :param per_page: Cuántos elementos se devuelven en cada página
            :return: Objeto 'pagination' con los miembros
        """
        return Miembro.query.order_by(Miembro.nombre.asc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
