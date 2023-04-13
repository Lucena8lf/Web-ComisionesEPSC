# Este fichero contiene métodos factoría para crear e inicializar la app y los
# distintos componentes y extensiones. (Aquí se suele definir un método factoría para
# crear la `app`, inicializar las diferentes extensiones,
# como el LoginManager() o el SQLAlchemy(), y registrar los blueprints)

import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()

# Definimos la ruta de la base de datos ya que da problemas
project_root = os.path.dirname(os.path.realpath(os.getcwd()))
db_path = os.path.join(project_root, "database", "comisiones.db")


def create_app():
    # Método factoria que inicializa la app

    app = Flask(__name__)
    app.config[
        "SECRET_KEY"
    ] = "7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe"
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/comisiones.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        app.root_path, "database", "comisiones.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializamos con init_app base de datos, migrate, etc.
    login_manager.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

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

    # from .public import public_bp
    # app.register_blueprint(public_bp)

    # with app.app_context():
    #    print(app.config["SQLALCHEMY_DATABASE_URI"])
    #    db.create_all()

    return app
