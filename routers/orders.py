# routers/orders.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from db import get_db
from models import Product, Order, OrderLine
from schemas import OrderCreate, OrderOut, OrderItemOut

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.get("/ping")
def ping():
    return {"ok": True}


@router.post("/", response_model=OrderOut)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    if not payload.items:
        raise HTTPException(status_code=400, detail="EMPTY_CART")

    product_map: dict[int, Product] = {}
    total = 0

    # Validar productos y calcular total
    for item in payload.items:
        if item.qty <= 0:
            raise HTTPException(status_code=400, detail="INVALID_QTY")

        product = db.get(Product, item.product_id)
        if not product or not product.active:
            raise HTTPException(status_code=400, detail=f"PRODUCT_{item.product_id}_NOT_FOUND")

        if product.stock is not None and product.stock < item.qty:
            raise HTTPException(status_code=400, detail=f"PRODUCT_{item.product_id}_OUT_OF_STOCK")

        product_map[item.product_id] = product
        total += product.price * item.qty

    order = Order(
        email=payload.email,
        shipping_address=(payload.shipping_address or "").strip() or None,
        total=total,
    )
    db.add(order)
    db.flush()  # para tener order.id

    for item in payload.items:
        product = product_map[item.product_id]
        line = OrderLine(
            order_id=order.id,
            product_id=product.id,
            qty=item.qty,
            unit_price=product.price,
            subtotal=product.price * item.qty,
        )
        db.add(line)

        # Descontar stock
        if product.stock is not None:
            product.stock -= item.qty
            if product.stock < 0:
                product.stock = 0

    db.commit()
    db.refresh(order)

    items_out: List[OrderItemOut] = []
    for line in order.lines:
        items_out.append(
            OrderItemOut(
                product_id=line.product_id,
                product_name=line.product.name if line.product else "",
                qty=line.qty,
                unit_price=line.unit_price,
                subtotal=line.subtotal,
            )
        )

    return OrderOut(
        id=order.id,
        email=order.email,
        total=order.total,
        created_at=order.created_at,
        shipping_address=order.shipping_address,
        items=items_out,
    )


@router.get("/by-email/{email}", response_model=List[OrderOut])
def list_orders_by_email(email: str, db: Session = Depends(get_db)):
    orders = (
        db.query(Order)
        .options(joinedload(Order.lines).joinedload(OrderLine.product))
        .filter(Order.email == email)
        .order_by(Order.created_at.desc())
        .all()
    )

    result: List[OrderOut] = []
    for o in orders:
        items_out: List[OrderItemOut] = []
        for line in o.lines:
            items_out.append(
                OrderItemOut(
                    product_id=line.product_id,
                    product_name=line.product.name if line.product else "",
                    qty=line.qty,
                    unit_price=line.unit_price,
                    subtotal=line.subtotal,
                )
            )

        result.append(
            OrderOut(
                id=o.id,
                email=o.email,
                total=o.total,
                created_at=o.created_at,
                shipping_address=o.shipping_address,
                items=items_out,
            )
        )

    return result
