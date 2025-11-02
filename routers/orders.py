# routers/orders.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models import Product
from schemas import OrderCreate

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.get("/ping")
def ping():
    return {"ok": True}

@router.post("/")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):  # <-- sin paréntesis
    total = 0
    detalles = []

    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Producto {item.product_id} no encontrado")
        if product.stock < item.qty:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para {product.name}")

        subtotal = product.price * item.qty
        total += subtotal
        detalles.append({"producto": product.name, "cantidad": item.qty, "subtotal": subtotal})

        product.stock -= item.qty
        db.add(product)

    db.commit()
    return {"email": order.email, "total": total, "detalles": detalles}
