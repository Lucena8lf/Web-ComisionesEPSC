import datetime

from datetime import date

from app import db

from app.miembro.models import Miembro, miembros_comisiones


class Comision(db.Model):
    __tablename__ = "comision"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), nullable=False)
    comentarios = db.Column(db.String(1000), nullable=True)
    fecha_apertura = db.Column(db.Date, nullable=False, default=date.today())
    fecha_cierre = db.Column(db.Date, nullable=True)

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
            :param miembros: Lista de los IDs y cargos de los miembros que se quiere añadir al crear la comisión
                * Si se crea vacía -> miembros=[]
                * Si se crea con miembros -> miembros=[ (id_miembro1, cargo1), (id_miembro2, cargo2), ...]
        """
        if not self.id:
            db.session.add(self)

            if miembros:
                # Si se ha introducido al menos un miembro habrá que añadir una tupla
                # en la tabla 'miembros_comisiones'. Se añaden tantas tuplas en la tabla
                # como miembros haya querido añadir el usuario

                for miembro_id in miembros:
                    # Vemos si el miembro existe (que sea activo ya lo hemos asegurado antes)
                    miembro = Miembro.get_by_id(miembro_id[0])

                    if miembro:
                        # Insertamos la tupla para ese miembro en 'miembros_comisiones'
                        db.session.execute(
                            db.text(
                                "INSERT INTO miembros_comisiones (id_miembro, id_comision, fecha_incorporacion, fecha_baja, cargo) "
                                "VALUES (:id_miembro, :id_comision, :fecha_incorporacion, :fecha_baja, :cargo)"
                            ),
                            {
                                "id_miembro": miembro.id,
                                "id_comision": self.id,
                                "fecha_incorporacion": self.fecha_apertura,
                                "fecha_baja": None,
                                "cargo": miembro_id[1],
                            },
                        )

        # Guardamos todas en la base de datos
        db.session.commit()

    def close(self, fecha_cierre, miembros_comision):
        """
        Método para cerrar una comisión
            :param fecha_cierre: fecha de cierre que el usuario ha decidido para la comisión
            :param miembros_comisión: lista de los IDs de todos los miembros que pertenecen a esa comisión
        """
        # La comisión no es borrada como tal, sino que se setea su fecha de cierre
        self.fecha_cierre = fecha_cierre

        # Automáticamente a todos los miembros actuales que no tengan fecha de baja
        # o tengan una fecha de baja posterior a la de cierre se les pondrá como
        # fecha de baja la fecha de cierre indicada
        for id_miembro in miembros_comision:
            # Excluimos los miembros que ya tienen una fecha de baja anterior a la
            # fecha de cierre
            fechas_baja = db.session.execute(
                db.text(
                    "SELECT fecha_baja FROM miembros_comisiones WHERE id_miembro=(:id_miembro) AND id_comision=(:id_comision)"
                ),
                {
                    "id_miembro": id_miembro,
                    "id_comision": self.id,
                },
            ).fetchall()

            # Un miembro puedo tener varias fechas de incorporación y de cierre en la misma comisión
            # por lo que debemos recorrerlas todas
            for fecha_baja in fechas_baja:
                if fecha_baja[0]:
                    # Obtenemos fecha baja como un str, por lo que la transformamos
                    formato = "%Y-%m-%d"
                    fecha_baja = datetime.datetime.strptime(
                        fecha_baja[0], formato
                    ).date()
                    if fecha_baja > fecha_cierre:
                        db.session.execute(
                            db.text(
                                "UPDATE miembros_comisiones SET fecha_baja=(:fecha_cierre) WHERE id_miembro=(:id_miembro) AND id_comision=(:id_comision) AND fecha_baja=(:fecha_baja)"
                            ),
                            {
                                "fecha_cierre": fecha_cierre,
                                "id_miembro": id_miembro,
                                "id_comision": self.id,
                                "fecha_baja": fecha_baja,
                            },
                        )
                else:
                    # Si no tiene fecha de baja le ponemos la fecha de cierre como fecha de baja
                    db.session.execute(
                        db.text(
                            "UPDATE miembros_comisiones SET fecha_baja=(:fecha_cierre) WHERE id_miembro=(:id_miembro) AND id_comision=(:id_comision) AND fecha_baja IS (:fecha_baja)"
                        ),
                        {
                            "fecha_cierre": fecha_cierre,
                            "id_miembro": id_miembro,
                            "id_comision": self.id,
                            "fecha_baja": None,
                        },
                    )

        # Guardamos en la base de datos
        db.session.commit()

    def update(
        self,
        fechas_incorporacion_nuevas=None,
        fechas_baja_nuevas=None,
        cargos_nuevos=None,
        motivos_baja_nuevos=None,
        miembros_nuevos=None,
    ):
        """
        Método para actualizar la información de una comisión
            :param fechas_incorporacion_nuevas: Lista de tuplas con la nueva fecha de incorporacion de cada
            miembro y la ID de la tupla asociada a ella
                * Lista formada por (id_tupla, fecha_incorporacion)
            :param fechas_baja_nuevas: Lista de tuplas con la nueva fecha de baja de cada
            miembro y la ID de la tupla asociada a ella
                * Lista formada por (id_tupla, fecha_baja)
            :param cargos_nuevos: Lista de tuplas con los nuevos cargos de cada miembro y la ID
            de la tupla asociada a ella
                * Lista formada por (id_tupla, cargo)
            :param motivos_baja_nuevos: Lista de tuplas con los nuevos motivos de baja de cada miembro y
            la ID de la tupla asociada a ella
                * Lista formada por (id_tupla, motivo_baja)
            :param miembros_nuevos: Lista de los nuevos miembros que se quieren
            añadir a la comisión con sus respectivas fechas de incorporación, fechas de baja, cargos y motivos de baja.
                * Lista formada por: (id_miembro, fecha_incorporacion, fecha_baja, cargo, motivo_baja)
            :return: Devuelve None si ha ido todo correcto o un mensaje de error con el error
            que haya ocurrido al hacer las sentencias.
        """

        message = None
        formato = "%Y-%m-%d"  # Formato para formatear fechas

        # Primero comprobamos si se ha modificado una fecha de incorporación a alguno de los
        # miembros ya existentes
        if fechas_incorporacion_nuevas:
            # La lista tiene tuplas de la forma: (id_tupla, fecha_incorporacion)
            for element in fechas_incorporacion_nuevas:
                # Obtenemos la fecha de baja de ese miembro
                fecha_baja = db.session.execute(
                    db.text(
                        "SELECT fecha_baja, id_miembro FROM miembros_comisiones WHERE id=(:id_tupla)"
                    ),
                    {
                        "id_tupla": element[0],
                    },
                ).fetchone()

                id_miembro = fecha_baja[1]

                # Comprobamos si esa fecha es posterior a la fecha de incorporación que quiere establecer
                if not fecha_baja[0] or fecha_baja[0] > element[1]:
                    # Comprobamos también que la fecha de incorporación que actualiza sea posterior a la última
                    # fecha de baja de ese miembro en la comisión
                    # Solo comprobamos esto en tuplas ya completas y pasadas, es decir, en las que
                    # ya se ha incorporado y dado de baja el miembro
                    if not fecha_baja[0]:
                        last_fecha_baja = db.session.execute(
                            db.text(
                                "SELECT MAX(fecha_baja) FROM miembros_comisiones WHERE id_miembro=(:id_miembro) AND id_comision=(:id_comision)"
                            ),
                            {
                                "id_miembro": id_miembro,
                                "id_comision": self.id,
                            },
                        ).first()

                        if last_fecha_baja[0]:
                            last_fecha_baja = datetime.datetime.strptime(
                                last_fecha_baja[0], formato
                            ).date()
                        else:
                            last_fecha_baja = None

                        # Para que se pueda añadir el miembro la fecha de incorporación debe ser posterior
                        # a la última fecha de baja O que sea la primera vez que se añade a ese miembro a la comisión,
                        # es decir, que last_fecha_baja=None
                        #
                        # La fecha de incorporación es un str por lo que lo debemos convertir para compararlo
                        if (
                            last_fecha_baja is None
                            or datetime.datetime.strptime(element[1], formato).date()
                            >= last_fecha_baja
                        ):
                            db.session.execute(
                                db.text(
                                    "UPDATE miembros_comisiones SET fecha_incorporacion=(:fecha_incorporacion) WHERE id=(:id_tupla)"
                                ),
                                {
                                    "fecha_incorporacion": element[1],
                                    "id_tupla": element[0],
                                },
                            )
                        else:
                            miembro = Miembro.get_by_id(id_miembro)
                            message = f"La nueva fecha de incorporación del miembro '{miembro.nombre} {miembro.apellidos}' es anterior a su última fecha de baja. Por favor, comprueba la nueva fecha de incorporación del miembro."
                    else:
                        db.session.execute(
                            db.text(
                                "UPDATE miembros_comisiones SET fecha_incorporacion=(:fecha_incorporacion) WHERE id=(:id_tupla)"
                            ),
                            {
                                "fecha_incorporacion": element[1],
                                "id_tupla": element[0],
                            },
                        )
                else:
                    message = "La fecha de incorporación debe ser anterior a la fecha de baja. Por favor, revise los datos introducidos."

        # Ahora comprobamos si se ha añadido una fecha de baja de alguno de los miembros
        # ya existentes
        if fechas_baja_nuevas:
            # La lista tiene tuplas de la forma: (id_tupla, fecha_baja)
            for element in fechas_baja_nuevas:
                # Obtenemos la fecha de incorporación de ese miembro
                fecha_incorporacion = db.session.execute(
                    db.text(
                        "SELECT fecha_incorporacion, id_miembro FROM miembros_comisiones WHERE id=(:id_tupla)"
                    ),
                    {
                        "id_tupla": element[0],
                    },
                ).fetchone()

                id_miembro = fecha_incorporacion[1]

                # Comprobamos si esa fecha es anterior a la fecha de baja que quiere establecer
                if fecha_incorporacion and fecha_incorporacion[0] < element[1]:
                    # Ya comprobamos que la fecha de incorporación es posterior a la última fecha
                    # de baja, y se comprueba que la fecha de baja siempre es posterior a la de incorporación
                    db.session.execute(
                        db.text(
                            "UPDATE miembros_comisiones SET fecha_baja=(:fecha_baja) WHERE id=(:id_tupla)"
                        ),
                        {
                            "fecha_baja": element[1],
                            "id_tupla": element[0],
                        },
                    )

                else:
                    message = "La fecha de baja debe ser posterior a la fecha de incorporación. Por favor, revise los datos introducidos."

        # Comprobamos si se han actualizado o añadido algunos de los cargos de los miembros ya existentes
        if cargos_nuevos:
            for element in cargos_nuevos:
                db.session.execute(
                    db.text(
                        "UPDATE miembros_comisiones SET cargo=(:cargo) WHERE id=(:id_tupla)"
                    ),
                    {
                        "cargo": element[1],
                        "id_tupla": element[0],
                    },
                )

        # Comprobamos si se han actualizado o añadido algunos de los motivos de baja de los miembros ya existentes
        if motivos_baja_nuevos:
            for element in motivos_baja_nuevos:
                db.session.execute(
                    db.text(
                        "UPDATE miembros_comisiones SET motivo_baja=(:motivo_baja) WHERE id=(:id_tupla)"
                    ),
                    {
                        "motivo_baja": element[1],
                        "id_tupla": element[0],
                    },
                )

        if miembros_nuevos:
            for miembro_data in miembros_nuevos:
                if miembro_data[0] == "":
                    # Por si ha añadido un miembro vacío
                    continue
                miembro = Miembro.get_by_id(miembro_data[0])
                # Ambas fechas se nos pasan como string, por lo que para compararlas las pasamos a tipo datetime.date
                miembro_date_incorporacion = datetime.datetime.strptime(
                    miembro_data[1], formato
                ).date()
                miembro_date_baja = ""  # Para evitar errores al estar en un if
                if miembro_data[2] != "":
                    miembro_date_baja = datetime.datetime.strptime(
                        miembro_data[2], formato
                    ).date()

                if miembro:
                    # Comprobamos si la fecha de incorporacion que quiere añadir es igual a posterior a
                    # la última fecha de baja de ese miembro en esa comisión
                    # Por lo que recuperamos la última fecha de baja de ese miembro en esa comisión
                    last_fecha_baja = db.session.execute(
                        db.text(
                            "SELECT MAX(fecha_baja) FROM miembros_comisiones WHERE id_miembro=(:id_miembro) AND id_comision=(:id_comision)"
                        ),
                        {
                            "id_miembro": miembro.id,
                            "id_comision": self.id,
                        },
                    ).first()

                    if last_fecha_baja[0]:
                        last_fecha_baja = datetime.datetime.strptime(
                            last_fecha_baja[0], formato
                        ).date()
                    else:
                        last_fecha_baja = None

                    # Para que se pueda añadir el miembro la fecha de incorporación debe ser posterior
                    # a la última fecha de baja O que sea la primera vez que se añade a ese miembro a la comisión,
                    # es decir, que last_fecha_baja=None
                    if (
                        last_fecha_baja is None
                        or miembro_date_incorporacion >= last_fecha_baja
                    ):
                        if (
                            miembro_date_baja == ""
                            or miembro_date_baja > miembro_date_incorporacion
                        ):
                            # Insertamos la tupla para ese miembro en 'miembros_comisiones'
                            db.session.execute(
                                db.text(
                                    "INSERT INTO miembros_comisiones (id_miembro, id_comision, fecha_incorporacion, fecha_baja, cargo, motivo_baja) "
                                    "VALUES (:id_miembro, :id_comision, :fecha_incorporacion, :fecha_baja, :cargo, :motivo_baja)"
                                ),
                                {
                                    "id_miembro": miembro.id,
                                    "id_comision": self.id,
                                    "fecha_incorporacion": miembro_date_incorporacion,  # Se recoge ahora del formulario
                                    "fecha_baja": None
                                    if miembro_date_baja == ""
                                    else miembro_date_baja,  # Se recoge ahora del formulario
                                    "cargo": None
                                    if miembro_data[3] == ""
                                    else miembro_data[3],
                                    "motivo_baja": None
                                    if miembro_data[4] == ""
                                    else miembro_data[4],
                                },
                            )
                        else:
                            message = "La fecha de baja debe ser posterior a la fecha de incorporación. Por favor, revise los datos introducidos de los nuevos miembros añadidos."
                    else:
                        message = f"La nueva fecha de incorporación del miembro '{miembro.nombre} {miembro.apellidos}' es anterior a su última fecha de baja. Por favor, comprueba la nueva fecha de incorporación del miembro."

        db.session.commit()

        return message

    def check_new_fecha_apertura(self, new_fecha_apertura):
        """
        Método que es llamado si el usuario ha actualizado la fecha de apertura de la comisión.
        Si ha cambiado la fecha de apertura comprobamos que todos los miembros que tengan
        su fecha de incorporación ANTERIOR a esta fecha de apertura, se establezca por defecto
        que tenga como fecha de incorporación la fecha de apertura de la comisión
            :param new_fecha_apertura: nueva fecha de apertura para la comisión
        """

        # Obtenemos las IDs de los miembros de la comisión que tienen su fecha_incorporacion < new_fecha_apertura
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

    @staticmethod
    def get_all_paginated(page=1, per_page=20):
        """
        Método que devuelve las comisiones paginadas
            :param page: Página a partir de la cual se obtienen los resultados
            :param per_page: Cuántos elementos se devuelven en cada página
            :return: Objeto 'pagination' con las comisiones
        """
        return Comision.query.order_by(Comision.nombre.asc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
