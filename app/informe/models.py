from app import db


class Informe(db.Model):
    __tablename__ = "informe"

    id = db.Column(db.Integer, primary_key=True)
    secretario = db.Column(db.String(256), nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    tipo = db.Column(db.Enum("escuela", "comision"), nullable=False)
    dni_miembro = db.Column(db.String(20), db.ForeignKey("miembro.dni"), nullable=False)

    def __repr__(self):
        """
        Sobrecargamos el método __repr__ para representar como queramos los objetos
        de esta clase
        """
        return f"<Informe {Informe.correo}>"
