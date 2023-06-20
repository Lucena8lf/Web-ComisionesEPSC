import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from app.common.filters import format_datetime


login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()


def create_app(settings_module):
    # Método factoria que inicializa la app

    app = Flask(__name__, instance_relative_config=True)

    # Cargamos el archivo de configuración indicado por la variable de entorno APP
    app.config.from_object(settings_module)

    # Cargamos la configuración de la carpeta 'instance'
    app.config.from_pyfile("config.py", silent=True)

    # Inicializamos con init_app base de datos, migrate, etc.
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    # Registramos los filtros
    register_filters(app)

    # Registramos todos los Blueprints que tengamos
    from .miembro import miembro_bp

    app.register_blueprint(miembro_bp)

    from .comision import comision_bp

    app.register_blueprint(comision_bp)

    from .informe import informe_bp

    app.register_blueprint(informe_bp)

    from .auth import auth_bp

    app.register_blueprint(auth_bp)

    from .main import main_bp

    app.register_blueprint(main_bp)

    # with app.app_context():
    #    print(app.config["SQLALCHEMY_DATABASE_URI"])
    #    db.create_all()

    # Manejador de errores
    error_handlers(app)

    return app


def register_filters(app):
    """
    Función que registra la función format_datetime() como filtro de Jinja2
    """
    app.jinja_env.filters["datetime"] = format_datetime


def error_handlers(app):
    """
    Función para registrar manejadores de errores personalizados
    """

    @app.errorhandler(404)
    def error_404_handler(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def error_500_handler(e):
        return render_template("500.html"), 500
