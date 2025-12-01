# schemas.py
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict  # Pydantic v2


# ========================
# Productos
# ========================
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


# ========================
# Órdenes (entrada)
# ========================
class OrderLineIn(BaseModel):
    product_id: int
    qty: int


class OrderCreate(BaseModel):
    email: EmailStr
    items: List[OrderLineIn]
    shipping_address: Optional[str] = None   # 👈 nueva


# ========================
# Órdenes (salida)
# ========================
class OrderItemOut(BaseModel):
    product_id: int
    product_name: str
    qty: int
    unit_price: int
    subtotal: int


class OrderOut(BaseModel):
    id: int
    email: EmailStr
    total: int
    created_at: Optional[datetime] = None
    shipping_address: Optional[str] = None
    items: List[OrderItemOut] = []

    model_config = ConfigDict(from_attributes=True)


# ========================
# Auth / Usuarios
# ========================
class UserOut(BaseModel):
    id: int
    email: EmailStr
    shipping_address: Optional[str] = None    # 👈 para perfil

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
