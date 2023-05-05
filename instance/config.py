# instance/config.py
import os

from config.default import BASE_DIR

# Base de datos real
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
    BASE_DIR, "app", "database", "comisiones.db"
)
