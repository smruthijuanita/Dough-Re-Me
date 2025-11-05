"""Pydantic schemas for Order."""
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


class OrderItemBase(BaseModel):
    """Base schema for OrderItem."""
    product_id: int
    quantity: int = Field(..., gt=0)


class OrderItemCreate(OrderItemBase):
    """Schema for creating an order item."""
    pass


class OrderItemOut(OrderItemBase):
    """Schema for order item response."""
    id: int
    price: float
    
    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    """Base schema for Order."""
    customer_name: str = Field(..., max_length=100)
    customer_email: EmailStr
    customer_phone: Optional[str] = Field(None, max_length=20)


class OrderCreate(OrderBase):
    """Schema for creating a new order."""
    items: List[OrderItemCreate]


class OrderOut(OrderBase):
    """Schema for order response."""
    id: int
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        orm_mode = True
