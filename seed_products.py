# seed_products.py
import json
from sqlalchemy.orm import Session
from db import SessionLocal, engine
from models import Base, Product

# Crear las tablas si no existen (solo por seguridad)
Base.metadata.create_all(bind=engine)

# Cargar los productos desde el JSON
with open("products.json", encoding="utf-8-sig") as f:

    data = json.load(f)
    products = data["value"]

db: Session = SessionLocal()

for p in products:
    existing = db.query(Product).filter_by(slug=p["slug"]).first()
    if not existing:
        product = Product(
            slug=p["slug"],
            name=p["name"],
            description=p["description"],
            price=p["price"],
            color=p["color"],
            stock=p["stock"],
            active=p["active"]
        )
        db.add(product)

db.commit()
db.close()
print("✅ Productos insertados correctamente.")
