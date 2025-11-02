from fastapi import APIRouter

router = APIRouter(prefix="/api/orders", tags=["orders"])

# Más adelante:
# @router.post("", response_model=OrderOut)
# def create_order(payload: OrderCreate, ...): ...

