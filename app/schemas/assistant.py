"""Schemas for Assistant chat API."""
from __future__ import annotations

from typing import List, Optional, Literal
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

from app.schemas.product import ProductOut


class IntentEnum(str, Enum):
    recommend_products = "recommend_products"
    order_inquiry = "order_inquiry"
    greeting = "greeting"
    fallback = "fallback"


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(..., max_length=2000)


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    top_n: int = Field(5, ge=1, le=20)
    # Optional coarse filters
    category: Optional[str] = None
    price_min: Optional[float] = Field(None, ge=0)
    price_max: Optional[float] = Field(None, ge=0)


class AssistantReply(BaseModel):
    intent: IntentEnum
    text: str
    suggested_products: List[ProductOut] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: AssistantReply

    model_config = ConfigDict(from_attributes=True)
