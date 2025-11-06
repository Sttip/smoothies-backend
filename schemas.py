# schemas.py
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict  # Pydantic v2


# -------- Productos
class ProductOut(BaseModel):
    id: int
    slug: str
    name: str
    description: Optional[str] = None
    price: int
    color: str
    stock: int
    active: bool

    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(BaseModel):
    stock: int


# -------- Órdenes
class OrderLineIn(BaseModel):
    product_id: int
    qty: int


class OrderCreate(BaseModel):
    email: EmailStr
    items: List[OrderLineIn]


# (opcional) por si quieres responder con un ID de orden
class OrderOut(BaseModel):
    id: int
    email: EmailStr
    total: int

    model_config = ConfigDict(from_attributes=True)


# -------- Auth (nuevo)
class UserOut(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class RegisterIn(BaseModel):
    email: EmailStr
    password: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    ok: bool
    user: Optional[UserOut] = None
    error: Optional[str] = None
