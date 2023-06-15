# instance/config.py
import os

from config.default import BASE_DIR

# Database
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
    BASE_DIR, "app", "database", "comisiones.db"
)
