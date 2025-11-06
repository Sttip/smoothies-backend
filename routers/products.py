# routers/products.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, text
from pydantic import BaseModel

from db import get_db
from models import Product
from schemas import ProductOut

router = APIRouter(prefix="/api/products", tags=["products"])


# --- 📦 Listar todos los productos activos ---
@router.get("", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    try:
        stmt = select(Product).where(Product.active == True)
        rows = db.execute(stmt).scalars().all()
        return [ProductOut.model_validate(r) for r in rows]
    except Exception as e:
        print("❌ /api/products error:", repr(e))
        raise HTTPException(status_code=500, detail="PRODUCTS_QUERY_FAILED")


# --- 🧠 Chequeo rápido de conexión con la DB ---
@router.get("/_dbcheck")
def db_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"db": "ok"}
    except Exception as e:
        import traceback
        print("❌ DB check error:", repr(e))
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="DB_ERROR")


# --- 🧩 Esquema para actualización parcial de productos (stock) ---
class ProductUpdate(BaseModel):
    stock: int


# --- 🔄 Endpoint para actualizar stock ---
@router.put("/{product_id}", response_model=ProductOut)
def update_product_stock(product_id: int, data: ProductUpdate, db: Session = Depends(get_db)):
    """
    Actualiza el stock de un producto por su ID.
    """
    try:
        product = db.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        product.stock = data.stock
        db.commit()
        db.refresh(product)
        return ProductOut.model_validate(product)

    except Exception as e:
        print("❌ Error al actualizar producto:", repr(e))
        raise HTTPException(status_code=500, detail="PRODUCT_UPDATE_FAILED")
