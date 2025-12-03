"""Assistant API: Llama 3 powered intent detection and order processing."""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter
import os
import json
from app.core.config import settings
from app.llm_client import llm
from app.product_service import products_by_ids
from app.db.supabase import get_client

from app.schemas.assistant import ChatRequest, ChatResponse, IntentEnum
# No local DB session; using Supabase only
# SQLAlchemy models removed; using Supabase now
from app.schemas.product import ProductOut
from app.core.email import send_order_confirmation_email

router = APIRouter()

# Initialize Groq client
# In a real app, this should be in a dependency or core module
# Using custom Groq HTTP client llm (reads GROQ_API_KEY from .env)

SYSTEM_PROMPT = """You are a helpful bakery assistant for 'Dough-Re-Me'. 
Your goal is to help customers place orders, recommend products, or answer questions.

You have access to the following products (IDs are important):
{products_list}

When a user wants to order:
1. Identify the product they want (fuzzy match to the list).
2. Extract quantity (default to 1).
3. Extract customer details: Name, Email, Phone.
4. If any detail is missing (Product, Quantity, Name, Email, Phone), ask for it politely.
5. If ALL details are present, output a JSON object with the key "action": "create_order" and the details.

Output Format:
Always return a JSON object.
{{
  "intent": "create_order" | "recommend_products" | "greeting" | "order_inquiry" | "fallback",
  "reply_text": "The text to show the user",
  "order_details": {{
      "product_id": 123,
      "quantity": 2,
      "customer_name": "John",
      "customer_email": "john@example.com",
      "customer_phone": "1234567890"
  }} (only if intent is create_order and ALL details are present, otherwise null),
  "missing_info": ["product", "customer_name", ...] (list of missing fields if intent is create_order)
}}

Example 1 (Incomplete Order):
User: "I want a cake"
JSON:
{{
  "intent": "create_order",
  "reply_text": "Which cake would you like? We have Chocolate Cake and Vanilla Sponge.",
  "order_details": null,
  "missing_info": ["product_id"]
}}

Example 2 (Complete Order):
User: "I want 2 Chocolate Cakes. Name is Alice, alice@test.com, 555-1234"
JSON:
{{
  "intent": "create_order",
  "reply_text": "Order placed! I've sent a confirmation to alice@test.com.",
  "order_details": {{
      "product_id": 1,
      "quantity": 2,
      "customer_name": "Alice",
      "customer_email": "alice@test.com",
      "customer_phone": "555-1234"
  }},
  "missing_info": []
}}
"""

# Build products context from Supabase for the system prompt
def get_products_context() -> str:
    try:
        supa = get_client()
        resp = supa.table("desserts").select("id,name,price").limit(50).execute()
        rows = resp.data or []
        return "\n".join([f"- ID {r.get('id')}: {r.get('name')} (${float(r.get('price', 0)):.2f})" for r in rows])
    except Exception:
        return ""

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Chat endpoint using Llama 3."""
    
    # 1. Prepare Context
    products_context = get_products_context()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT.format(products_list=products_context)}
    ]
    # Add conversation history
    for m in request.messages:
        messages.append({"role": m.role, "content": m.content})
        
    # 2. Call Groq via custom client
    try:
        response_text = llm.chat(
            system_prompt=SYSTEM_PROMPT,
            messages=messages,
            temperature=0.0,
            max_tokens=512
        )
        data = json.loads(response_text)
    except Exception as e:
        print(f"LLM Error: {e}")
        # Fallback
        friendly = "Sorry, my assistant service is not configured. Please set GROQ_API_KEY in .env and restart." if "Missing GROQ_API_KEY" in str(e) or "invalid_api_key" in str(e).lower() else "Sorry, I'm having trouble connecting to my brain right now. Please try again."
        return ChatResponse(reply={
            "intent": IntentEnum.fallback,
            "text": friendly,
            "suggested_products": []
        })

    intent = IntentEnum(data.get("intent", "fallback"))
    reply_text = data.get("reply_text", "")
    order_details = data.get("order_details")
    
    suggested: List[ProductOut] = []

    # 3. Handle Actions
    if intent == IntentEnum.create_order and order_details:
        # Create order and items in Supabase
        try:
            supa = get_client()
            o_resp = (
                supa.table("orders")
                .insert({
                    "customer_name": order_details.get("customer_name"),
                    "customer_email": order_details.get("customer_email"),
                    "customer_phone": order_details.get("customer_phone"),
                    "total_amount": order_details.get("total_amount", 0),
                    "status": "pending",
                })
                .select("id")
                .execute()
            )
            order_id = (o_resp.data or [{}])[0].get("id")
            if order_id:
                items = order_details.get("items") or []
                items_payload = [
                    {
                        "order_id": order_id,
                        "product_id": it.get("product_id"),
                        "quantity": it.get("quantity", 1),
                        "price": it.get("price", 0),
                    }
                    for it in items
                    if it.get("product_id") is not None
                ]
                if items_payload:
                    supa.table("order_items").insert(items_payload).execute()
                # Send email with minimal order details
                cust_email = order_details.get("customer_email")
                if cust_email:
                    send_order_confirmation_email(
                        cust_email,
                        {
                            "id": order_id,
                            "customer_name": order_details.get("customer_name"),
                            "items": items_payload,
                            "total_amount": order_details.get("total_amount", 0),
                        },
                    )
        except Exception:
            pass
    elif intent == IntentEnum.recommend_products:
        # Map product_ids from model if provided; else fallback to top 3
        ids = data.get("product_ids") or []
        if isinstance(ids, list) and ids:
            suggested = products_by_ids(ids)
        else:
            try:
                supa = get_client()
                resp = supa.table("desserts").select("id,name,price,img,description,category,in_stock").limit(3).execute()
                rows = resp.data or []
                suggested = [
                    ProductOut(
                        id=row["id"],
                        name=row.get("name"),
                        price=float(row.get("price", 0)),
                        img=row.get("img"),
                        description=row.get("description"),
                        category=row.get("category"),
                        in_stock=bool(row.get("in_stock", True)),
                    )
                    for row in rows
                ]
            except Exception:
                suggested = []

    return ChatResponse(reply={"intent": intent, "text": reply_text, "suggested_products": suggested})
