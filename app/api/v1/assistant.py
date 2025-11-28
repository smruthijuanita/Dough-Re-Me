"""Assistant API: simple intent detection and product recommendations."""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.assistant import ChatRequest, ChatResponse, IntentEnum
from app.db.session import get_db
from app.models.product import Product
from app.schemas.product import ProductOut

router = APIRouter()


def detect_intent(text: str) -> IntentEnum:
    t = text.lower()
    if any(w in t for w in ["recommend", "suggest", "what should i", "i want"]):
        return IntentEnum.recommend_products
    if any(w in t for w in ["order", "status", "track", "where is my"]):
        return IntentEnum.order_inquiry
    if any(w in t for w in ["hi", "hello", "hey", "good morning", "good evening"]):
        return IntentEnum.greeting
    return IntentEnum.fallback


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """Simple chat endpoint that returns an intent and suggested products."""
    # Use last user message
    last_user = None
    for m in reversed(request.messages):
        if m.role == "user":
            last_user = m.content
            break
    if not last_user:
        last_user = request.messages[-1].content if request.messages else ""

    intent = detect_intent(last_user)
    reply_text = """Sorry, I didn't quite get that. You can ask me to recommend desserts or check order status."""
    suggested: List[ProductOut] = []

    if intent == IntentEnum.recommend_products:
        # Simple filters: by category and price range
        q = db.query(Product)
        if request.category:
            q = q.filter(Product.category == request.category)
        if request.price_min is not None:
            q = q.filter(Product.price >= request.price_min)
        if request.price_max is not None:
            q = q.filter(Product.price <= request.price_max)
        products = q.limit(request.top_n).all()
        suggested = [ProductOut.model_validate(p) for p in products]
        reply_text = f"Here are {len(suggested)} desserts you might like." if suggested else "I couldn't find desserts matching that filter."
    elif intent == IntentEnum.greeting:
        reply_text = "Hi! I can help recommend desserts or assist with your order. What would you like?"
    elif intent == IntentEnum.order_inquiry:
        reply_text = "Please provide your order id and I'll look it up (order-tracking not fully implemented)."

    return ChatResponse(reply={"intent": intent, "text": reply_text, "suggested_products": suggested})
