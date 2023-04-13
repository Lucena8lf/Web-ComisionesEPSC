from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Administrativo(db.Model, UserMixin):
    __tablename__ = "administrativo"

    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        """
        Sobrecargamos el método __repr__ para representar como queramos los objetos
        de esta clase
        """
        return f"<Administrativo {self.correo}>"

    def set_password(self, password):
        """
        Método para setear la contraseña del administrativo con su respectivo hash
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Método para comprobar si la contraseña introducida es correcta
        """
        return check_password_hash(self.password, password)

    # def save(self):
    # No es necesario un método save() ya que no está contemplado que se puedan
    # crear administrativos

    @staticmethod
    def get_by_id(id):
        """
        Método que obtiene el administrativo a partir de su id
        """
        Administrativo.query.get(id)

    @staticmethod
    def get_by_correo(correo):
        """
        Método que obtiene el administrativo a partir de su correo
        """
        Administrativo.query.filter_by(correo=correo).first()
