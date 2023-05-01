import datetime

from app import db

from app.miembro.models import Miembro, miembros_comisiones


class Comision(db.Model):
    __tablename__ = "comision"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), nullable=False)
    comentarios = db.Column(db.String(1000), nullable=True)
    fecha_apertura = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow
    )
    fecha_cierre = db.Column(db.DateTime, nullable=True)

    miembros = db.relationship(
        "Miembro",
        secondary="miembros_comisiones",
        back_populates="comisiones",
    )

    def __repr__(self):
        """
        Sobrecargamos el método __repr__ para representar como queramos los objetos
        de esta clase
        """
        return f"<Comision {self.nombre}>"

    def save(self, miembros=None):
        """
        Método para crear una nueva comisión
            :param miembros: Lista de los IDs de los miembros que se quiere añadir al crear la comisión
                * Si se crea vacía -> miembros=[]
                * Si se crea con miembros -> miembros=[id_miembro1, id_miembro2, ...]
        """
        if not self.id:
            db.session.add(self)

            if miembros:
                # Si se ha introducido al menos un miembro habrá que añadir una tupla
                # en la tabla 'miembros_comisiones'. Se añaden tantas tuplas en la tabla
                # como miembros haya querido añadir el usuario

                # self.miembros.extend(miembros)

                for miembro_id in miembros:
                    # Vemos si el miembro existe (que sea activo ya lo hemos asegurado antes)
                    miembro = Miembro.get_by_id(miembro_id)

                    if miembro:
                        # Insertamos la tupla para ese miembro en 'miembros_comisiones'
                        db.session.execute(
                            db.text(
                                "INSERT INTO miembros_comisiones (id_miembro, id_comision, fecha_incorporacion, fecha_baja) "
                                "VALUES (:id_miembro, :id_comision, :fecha_incorporacion, :fecha_baja)"
                            ),
                            {
                                "id_miembro": miembro.id,
                                "id_comision": self.id,
                                "fecha_incorporacion": self.fecha_apertura,
                                "fecha_baja": None,
                            },
                        )

        # Guardamos todas en la base de datos
        db.session.commit()

    def close(self, fecha_cierre, miembros_comision):
        """
        Método para cerrar una comisión
            :param Fecha_cierre: fecha de cierre que el usuario ha decidido para la comisión
            :param Miembros_comisión: lista de los IDs de todos los miembros que pertenecen a esa comisión
        """
        # La comisión no es borrada como tal, sino que se setea su fecha de cierre
        self.fecha_cierre = fecha_cierre

        # Automáticamente a todos los miembros actuales se les pondrá como
        # fecha de baja la fecha de cierre
        for id_miembro in miembros_comision:
            db.session.execute(
                db.text(
                    "UPDATE miembros_comisiones SET fecha_baja=(:fecha_cierre) WHERE id_miembro=(:id_miembro) AND id_comision=(:id_comision)"
                ),
                {
                    "fecha_cierre": fecha_cierre,
                    "id_miembro": id_miembro,
                    "id_comision": self.id,
                },
            )

        # Guardamos en la base de datos
        db.session.commit()

    def update(
        self,
        fechas_incorporacion_nuevas=None,
        fechas_baja_nuevas=None,
        miembros_nuevos=None,
    ):
        """
        Método para actualizar la información de una comisión
            :param fechas_incorporacion_nuevas: Lista de tuplas con la nueva fecha de incorporacion de cada
            miembro y la ID del miembro asociada a ella
                * Lista formada por (id_miembro, fecha_incorporacion)
            :param fechas_baja_nuevas: Lista de tuplas con la nueva fecha de baja de cada
            miembro y la ID del miembro asociada a ella
                * Lista formada por (id_miembro, fecha_baja)
            :param miembros_nuevos: Lista de los nuevos miembros que se quieren
            añadir a la comisión con sus respectivas fechas de incorporación y baja.
                * Lista formada por: (id_miembro, fecha_incorporacion, fecha_baja)
            :return: Devuelve None si ha ido todo correcto o un mensaje de error con el error
            que haya ocurrido al hacer las sentencias.
        """

        message = None

        # Primero comprobamos si se ha modificado una fecha de incorporación a alguno de los
        # miembros ya existentes
        if fechas_incorporacion_nuevas:
            # La lista tiene tuplas de la forma: (IdMiembro, fecha_incorporacion)
            for element in fechas_incorporacion_nuevas:
                # Obtenemos la fecha de baja de ese miembro
                fecha_baja = db.session.execute(
                    db.text(
                        "SELECT fecha_baja FROM miembros_comisiones WHERE id_miembro=(:id_miembro) AND id_comision=(:id_comision)"
                    ),
                    {
                        "id_miembro": element[0],
                        "id_comision": self.id,
                    },
                ).fetchone()

                # Comprobamos si esa fecha es posterior a la fecha de incorporación que quiere establecer
                if not fecha_baja[0]:
                    db.session.execute(
                        db.text(
                            "UPDATE miembros_comisiones SET fecha_incorporacion=(:fecha_incorporacion) WHERE id_miembro=(:id_miembro) AND id_comision=(:id_comision)"
                        ),
                        {
                            "fecha_incorporacion": element[1],
                            "id_miembro": element[0],
                            "id_comision": self.id,
                        },
                    )
                elif fecha_baja[0] > element[1]:
                    db.session.execute(
                        db.text(
                            "UPDATE miembros_comisiones SET fecha_incorporacion=(:fecha_incorporacion) WHERE id_miembro=(:id_miembro) AND id_comision=(:id_comision)"
                        ),
                        {
                            "fecha_incorporacion": element[1],
                            "id_miembro": element[0],
                            "id_comision": self.id,
                        },
                    )
                else:
                    message = "La fecha de incorporación debe ser anterior a la fecha de baja. Por favor, revise los datos introducidos."

        # Ahora comprobamos si se ha añadido una fecha de baja de alguno de los miembros
        # ya existentes
        if fechas_baja_nuevas:
            # La lista tiene tuplas de la forma: (IdMiembro, fecha_baja)
            for element in fechas_baja_nuevas:
                # Obtenemos la fecha de incorporación de ese miembro
                fecha_incorporacion = db.session.execute(
                    db.text(
                        "SELECT fecha_incorporacion FROM miembros_comisiones WHERE id_miembro=(:id_miembro) AND id_comision=(:id_comision)"
                    ),
                    {
                        "id_miembro": element[0],
                        "id_comision": self.id,
                    },
                ).fetchone()

                # Comprobamos si esa fecha es anterior a la fecha de baja que quiere establecer
                if fecha_incorporacion and fecha_incorporacion[0] < element[1]:
                    db.session.execute(
                        db.text(
                            "UPDATE miembros_comisiones SET fecha_baja=(:fecha_baja) WHERE id_miembro=(:id_miembro) AND id_comision=(:id_comision)"
                        ),
                        {
                            "fecha_baja": element[1],
                            "id_miembro": element[0],
                            "id_comision": self.id,
                        },
                    )
                else:
                    message = "La fecha de baja debe ser posterior a la fecha de incorporación. Por favor, revise los datos introducidos."

        if miembros_nuevos:
            for miembro_data in miembros_nuevos:
                miembro = Miembro.get_by_id(miembro_data[0])
                # Ambas fechas se nos pasan como string, por lo que para compararlas las pasamos a tipo datetime.date
                formato = "%Y-%m-%d"
                miembro_date_incorporacion = datetime.datetime.strptime(
                    miembro_data[1], formato
                ).date()
                miembro_date_baja = ""  # Para evitar errores al estar en un if
                if miembro_data[2] != "":
                    miembro_date_baja = datetime.datetime.strptime(
                        miembro_data[2], formato
                    ).date()

                if miembro:
                    if (
                        miembro_date_baja == ""
                        or miembro_date_baja > miembro_date_incorporacion
                    ):
                        # Insertamos la tupla para ese miembro en 'miembros_comisiones'
                        db.session.execute(
                            db.text(
                                "INSERT INTO miembros_comisiones (id_miembro, id_comision, fecha_incorporacion, fecha_baja) "
                                "VALUES (:id_miembro, :id_comision, :fecha_incorporacion, :fecha_baja)"
                            ),
                            {
                                "id_miembro": miembro.id,
                                "id_comision": self.id,
                                "fecha_incorporacion": miembro_date_incorporacion,  # Se recoge ahora del formulario
                                "fecha_baja": None
                                if miembro_date_baja == ""
                                else miembro_date_baja,  # Se recoge ahora del formulario
                            },
                        )
                    else:
                        message = "La fecha de baja debe ser posterior a la fecha de incorporación. Por favor, revise los datos introducidos."

        db.session.commit()

        return message

    def check_new_fecha_apertura(self, new_fecha_apertura):
        """
        Método que es llamado si el usuario ha actualizado la fecha de apertura de la comisión.
        Si ha cambiado la fecha de apertura comprobamos que todos los miembros que tengan
        su fecha de incorporación ANTERIOR a esta fecha de apertura, se establezca por defecto
        que tenga como fecha de incorporación la fecha de apertura de la comisión
        """
        # Comprobamos todas las tuplas de 'miembros_comisiones' y vemos todas las que
        # tengan id_comision=self.id y fecha_incorporacion < new_fecha_apertura. Esas serán las tuplas
        # que deberemos establecer como fecha_incorporacion = new_fecha_apertura

        # Obtenemos las IDs de los miembros de la comisión qeu tienen su fecha_incorporacion < new_fecha_apertura
        ids_miembros = db.session.execute(
            db.text(
                "SELECT id_miembro FROM miembros_comisiones WHERE id_comision=(:id_comision) AND fecha_incorporacion < (:fecha_apertura)"
            ),
            {
                "id_comision": self.id,
                "fecha_apertura": new_fecha_apertura,
            },
        ).fetchall()

        ids_miembros = [row[0] for row in ids_miembros]

        # Actualizamos la fecha_incorporacion de esos miembros
        if ids_miembros:
            for id_miembro in ids_miembros:
                db.session.execute(
                    db.text(
                        "UPDATE miembros_comisiones SET fecha_incorporacion=(:fecha_apertura) WHERE id_miembro=(:id_miembro)"
                    ),
                    {
                        "fecha_apertura": new_fecha_apertura,
                        "id_miembro": id_miembro,
                    },
                )

        db.session.commit()

    @staticmethod
    def get_by_id(id):
        """
        Método para obtener una comisión por su id
            :param id: ID de la comisión que se quiere obtener
            :return: Comisión obtenida
        """
        return Comision.query.get(id)

    @staticmethod
    def get_by_nombre(nombre):
        """
        Método para obtener una comisión por su nombre
            :param nombre: Nombre de la comisión que se quiere obtener
            :return: Comisión obtenida
        """
        return Comision.query.filter_by(nombre=nombre).first()
