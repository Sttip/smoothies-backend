from pydantic import BaseModel, EmailStr
from typing import List

# -------- Productos (salida) --------
class ProductOut(BaseModel):
    id: int
    slug: str
    name: str
    description: str
    price: int
    color: str
    stock: int
    class Config:
        from_attributes = True  # (orm_mode en Pydantic v1)

# -------- Órdenes (entrada/salida) --------
class OrderLineIn(BaseModel):
    product_id: int
    qty: int

class OrderCreate(BaseModel):
    email: EmailStr
    items: List[OrderLineIn]

class OrderOut(BaseModel):
    id: int
    email: EmailStr
    total: int
