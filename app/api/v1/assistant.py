"""Assistant API: simple intent detection and product recommendations."""
from typing import List, Optional, Tuple
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import re

from app.schemas.assistant import ChatRequest, ChatResponse, IntentEnum
from app.db.session import get_db
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.schemas.product import ProductOut
from app.core.email import send_order_confirmation_email

router = APIRouter()


def detect_intent(text: str) -> IntentEnum:
    t = text.lower()
    if any(w in t for w in ["show", "list", "all items", "all desserts", "menu", "what do you have", "available"]):
        return IntentEnum.recommend_products
    if any(w in t for w in ["recommend", "suggest", "what should i"]):
        return IntentEnum.recommend_products
    if any(w in t for w in ["buy", "purchase", "place an order", "i want to order", "order"]):
        return IntentEnum.create_order
    if any(w in t for w in ["status", "track", "where is my"]):
        return IntentEnum.order_inquiry
    if any(w in t for w in ["hi", "hello", "hey", "good morning", "good evening"]):
        return IntentEnum.greeting
    return IntentEnum.fallback

def extract_order_details(text: str, db: Session) -> Tuple[Optional[Product], int]:
    """Try to extract product and quantity from text."""
    # Simple quantity extraction
    qty_match = re.search(r'\b(\d+)\b', text)
    quantity = int(qty_match.group(1)) if qty_match else 1
    
    # Simple product extraction (fuzzy match would be better, but exact substring for now)
    products = db.query(Product).all()
    found_product = None
    text_lower = text.lower()
    
    for p in products:
        if p.name.lower() in text_lower:
            found_product = p
            break
            
    return found_product, quantity

def extract_customer_details(text: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Try to extract name, email, phone."""
    # Very basic extraction
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    email = email_match.group(0) if email_match else None
    
    phone_match = re.search(r'\b\d{10,}\b', text)
    phone = phone_match.group(0) if phone_match else None
    
    # Name is hard to extract without NLP, assuming comma separated or just taking the rest?
    # For this simple version, we might need to ask for them specifically or assume a format.
    # Let's try to find a name if it looks like "My name is X" or just assume the first part if comma separated.
    name = None
    if "name is" in text.lower():
        parts = text.lower().split("name is")
        if len(parts) > 1:
            name_part = parts[1].strip().split()[0]
            name = name_part.strip(",.").title()
    elif "," in text:
        parts = text.split(",")
        # Assume first part is name if not email/phone
        potential_name = parts[0].strip()
        if "@" not in potential_name and not potential_name.isdigit():
            name = potential_name
            
    return name, email, phone

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """Chat endpoint with order creation capability."""
    # Use last user message
    last_user_msg = None
    history_text = ""
    for m in request.messages:
        if m.role == "user":
            last_user_msg = m.content
        history_text += f" {m.content}" # Aggregate context
            
    if not last_user_msg:
        last_user_msg = request.messages[-1].content if request.messages else ""

    intent = detect_intent(last_user_msg)
    
    # Override intent if we are in the middle of an order flow (heuristic)
    # If previous bot message asked for details, we continue that flow.
    # For simplicity, we'll re-evaluate intent based on full context or just current message.
    # Let's stick to current message intent, but if fallback, check if we are providing details.
    
    if intent == IntentEnum.fallback:
        # Check if we might be providing order details
        if "email" in last_user_msg or "@" in last_user_msg or "name is" in last_user_msg:
             intent = IntentEnum.create_order
        elif any(char.isdigit() for char in last_user_msg) and "order" in history_text.lower():
             intent = IntentEnum.create_order

    reply_text = """Sorry, I didn't quite get that. You can ask me to recommend desserts, check order status, or place an order."""
    suggested: List[ProductOut] = []

    if intent == IntentEnum.recommend_products:
        # Simple filters: by category and price range
        q = db.query(Product).filter(Product.in_stock == True)
        if request.category:
            q = q.filter(Product.category == request.category)
        if request.price_min is not None:
            q = q.filter(Product.price >= request.price_min)
        if request.price_max is not None:
            q = q.filter(Product.price <= request.price_max)
        products = q.limit(request.top_n).all()
        suggested = [ProductOut.model_validate(p) for p in products]
        
        if "show" in last_user_msg.lower() or "list" in last_user_msg.lower() or "all" in last_user_msg.lower():
            reply_text = f"Here are all {len(suggested)} available desserts from our menu:"
        else:
            reply_text = f"Here are {len(suggested)} desserts you might like:" if suggested else "I couldn't find desserts matching that filter."
        
    elif intent == IntentEnum.greeting:
        reply_text = "Hi! I can help recommend desserts, check your order, or help you place a new order. What would you like?"
        
    elif intent == IntentEnum.order_inquiry:
        reply_text = "Please provide your order id and I'll look it up (order-tracking not fully implemented)."
        
    elif intent == IntentEnum.create_order:
        # 1. Extract Product
        product, quantity = extract_order_details(history_text, db) # Look at history for product
        
        # 2. Extract Customer Info
        name, email, phone = extract_customer_details(last_user_msg) # Look at current msg for details primarily
        if not name or not email:
             name, email, phone = extract_customer_details(history_text) # Fallback to history

        if not product:
            reply_text = "What would you like to order? We have cakes, cookies, and more."
            # Suggest some popular products
            products = db.query(Product).limit(3).all()
            suggested = [ProductOut.model_validate(p) for p in products]
        elif not name or not email:
            reply_text = f"Great! {quantity} x {product.name}. To finish the order, please provide your Name, Email, and Phone number."
        else:
            # Create Order
            total_amount = product.price * quantity
            order = Order(
                customer_name=name,
                customer_email=email,
                customer_phone=phone,
                total_amount=total_amount,
                status="pending"
            )
            db.add(order)
            db.flush()
            
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                price=product.price
            )
            db.add(order_item)
            db.commit()
            db.refresh(order)
            
            # Send Email
            order_details = {
                "id": order.id,
                "customer_name": name,
                "total_amount": total_amount,
                "items": [{"product_name": product.name, "quantity": quantity, "price": product.price}]
            }
            send_order_confirmation_email(email, order_details)
            
            reply_text = f"Order #{order.id} placed successfully! A confirmation email has been sent to {email}."

    return ChatResponse(reply={"intent": intent, "text": reply_text, "suggested_products": suggested})
