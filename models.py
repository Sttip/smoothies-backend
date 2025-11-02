from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    slug = Column(String(80), nullable=False, unique=True, index=True)  # ej: "berry-blast"
    name = Column(String(120), nullable=False)
    description = Column(Text, default="")
    price = Column(Integer, nullable=False)  # CLP en enteros
    color = Column(String(20), default="#cccccc")
    stock = Column(Integer, nullable=False, default=0)
    active = Column(Boolean, nullable=False, default=True)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    email = Column(String(180), nullable=False)   # comprador
    total = Column(Integer, nullable=False, default=0)
    lines = relationship("OrderLine", back_populates="order", cascade="all, delete-orphan")

class OrderLine(Base):
    __tablename__ = "order_lines"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    qty = Column(Integer, nullable=False)
    unit_price = Column(Integer, nullable=False)
    subtotal = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="lines")

    __table_args__ = (
        UniqueConstraint("order_id", "product_id", name="uq_order_product_once"),
    )
