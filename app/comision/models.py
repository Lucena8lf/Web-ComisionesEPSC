import datetime

from app import db


class Comision(db.Model):
    __tablename__ = "comision"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), nullable=False)
    comentarios = db.Column(db.String(1000), nullable=True)
    fecha_apertura = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow
    )
    fecha_cierre = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        """
        Sobrecargamos el método __repr__ para representar como queramos los objetos
        de esta clase
        """
        return f"<Comision {self.nombre}>"

    def save(self):
        """
        Método para crear una nueva comisión
        """
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        """
        Método para obtener una comisión por su id
        """
        return Comision.query.get(id)
