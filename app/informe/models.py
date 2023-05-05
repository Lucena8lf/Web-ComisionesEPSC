from app import db


class Informe(db.Model):
    __tablename__ = "informe"

    id = db.Column(db.Integer, primary_key=True)
    secretario = db.Column(db.String(256), nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    tipo = db.Column(db.Enum("escuela", "comision"), nullable=False)
    id_miembro = db.Column(db.Integer, db.ForeignKey("miembro.id"), nullable=False)

    def __repr__(self):
        """
        Sobrecargamos el método __repr__ para representar como queramos los objetos
        de esta clase
        """
        return f"<Informe {Informe.correo}>"

    def save(self):
        """
        Método para crear un nuevo informe
        """
        if not self.id:
            db.session.add(self)

        db.session.commit()

    @staticmethod
    def get_by_id(id):
        """
        Método para obtener un informe a partir de su id
        """
        return Informe.query.get(id)
