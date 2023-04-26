def format_datetime(value, format="short"):
    """
    Filtro para usar en plantillas de Jinja2 que transforma un datetime en str con formato.
    Formatos definidos:
        * short: dd/mm/aaaa
        * long: dd de mm de aaaa

    :param value: Fecha que se quiere transformar
    :param format: Formato que se desea utilizar
    :return: String que representa la fecha con el formato especificado
    """

    value_str = None
    if not value:
        value_str = ""
    if format == "short":
        value_str = value.strftime("%d/%m/%Y")
    elif format == "long":
        value_str = value.strftime("%d de %m de %Y")
    elif format == "form":
        # Formato utilizado por defecto por los formularios de HTML
        value_str = value.strftime("%Y-%m-%d")
    else:
        value_str = ""
    return value_str
