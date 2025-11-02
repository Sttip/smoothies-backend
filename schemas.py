# schemas.py
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict  # v2

class ProductOut(BaseModel):
    id: int
    slug: str
    name: str
    description: str | None = None
    price: int
    color: str
    stock: int
    active: bool

    # Pydantic v2: permite construir desde objetos ORM (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)

class OrderLineIn(BaseModel):
    product_id: int
    qty: int

class OrderCreate(BaseModel):
    email: EmailStr
    items: List[OrderLineIn]
