from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Product
from ..schemas import ProductOut

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("", response_model=list[ProductOut])
def list_products(q: str | None = Query(None), db: Session = Depends(get_db())):
    query = db.query(Product).filter(Product.active == True)
    if q:
        like = f"%{q.lower()}%"
        query = query.filter(Product.name.ilike(like) | Product.description.ilike(like))
    return query.order_by(Product.name.asc()).all()

@router.get("/{slug}", response_model=ProductOut)
def get_product(slug: str, db: Session = Depends(get_db())):
    p = db.query(Product).filter(Product.slug == slug, Product.active == True).first()
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return p
