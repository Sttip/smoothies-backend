# create_tables.py
"""
Script para crear las tablas en la base de datos PostgreSQL
usando los modelos definidos en models.py
"""

from db import engine            # usa db.py (no "database")
from models import Base          # Base declarative
# Importamos los modelos para que SQLAlchemy los registre
from models import Product, Order, OrderLine, User  # noqa: F401


def create_tables():
    print("🔧 Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas correctamente.")


if __name__ == "__main__":
    create_tables()
