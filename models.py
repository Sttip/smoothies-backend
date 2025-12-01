# models.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
    UniqueConstraint,
    DateTime,
    func,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# ---------------------------
# PRODUCTOS
# ---------------------------
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    slug = Column(String(80), nullable=False, unique=True, index=True)
    name = Column(String(120), nullable=False)
    description = Column(Text, default="")
    price = Column(Integer, nullable=False)  # precios en CLP (enteros)
    color = Column(String(20), default="#cccccc")
    stock = Column(Integer, nullable=False, default=0)
    active = Column(Boolean, nullable=False, default=True)

    def __repr__(self) -> str:  # solo debug
        return f"<Product id={self.id} name={self.name!r} stock={self.stock}>"


# ---------------------------
# PEDIDOS
# ---------------------------
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    email = Column(String(180), nullable=False)
    shipping_address = Column(Text, nullable=True)   # 👈 dirección de envío
    total = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    lines = relationship(
        "OrderLine",
        back_populates="order",
        cascade="all, delete-orphan",
    )


class OrderLine(Base):
    __tablename__ = "order_lines"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    qty = Column(Integer, nullable=False)
    unit_price = Column(Integer, nullable=False)
    subtotal = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="lines")
    product = relationship("Product")

    __table_args__ = (
        UniqueConstraint("order_id", "product_id", name="uq_order_product_once"),
    )


# ---------------------------
# USUARIOS
# ---------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(180), nullable=False, unique=True, index=True)
    shipping_address = Column(Text, nullable=True)   # 👈 dirección guardada en perfil
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
