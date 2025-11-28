"""Product model for bakery items."""
from sqlalchemy import Column, Integer, String, Float, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from app.db.base import Base


class Product(Base):
    """Product model representing bakery items."""
    __tablename__ = "desserts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    category = Column(String(50), nullable=True)
    img = Column(String(255), nullable=True)
    in_stock = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
