# 'miembros' se encargará de todo lo relacionado con los miembros en la aplicación

from flask import Blueprint

# En estos ficheros irán la inicialización de los Blueprints los cuales serán recogidos
# por el fichero "__init__.py" más general y los generará en la "app"
miembro_bp = Blueprint("miembro", __name__, template_folder="templates")

from . import routes
