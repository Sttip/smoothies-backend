# routers/products.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from db import get_db
from models import Product
from schemas import ProductOut

router = APIRouter(prefix="/api/products", tags=["products"])


# --- 📦 Listar todos los productos activos ---
@router.get("", response_model=List[ProductOut])
def list_products(db: Session = Depends(get_db)):
    stmt = select(Product).where(Product.active.is_(True)).order_by(Product.id.asc())
    products = db.execute(stmt).scalars().all()
    return [ProductOut.model_validate(p) for p in products]


# --- 📦 Obtener un producto por ID (no lo usa el front, pero sirve) ---
@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="PRODUCT_NOT_FOUND")
    return ProductOut.model_validate(product)
