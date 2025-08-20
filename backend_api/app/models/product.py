from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Integer, Numeric
from ..extensions import db

class Product(db.Model):
    """Product entity for demo CRUD (name, sku, price, stock)."""
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    sku: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0.00)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
