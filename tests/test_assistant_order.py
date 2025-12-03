import pytest
from unittest.mock import MagicMock, patch
from app.api.v1.assistant import detect_intent, extract_order_details, extract_customer_details, chat
from app.schemas.assistant import IntentEnum, ChatRequest, ChatMessage
# SQLAlchemy models removed; using Supabase now

def test_detect_intent():
    assert detect_intent("I want to buy a cake") == IntentEnum.create_order
    assert detect_intent("place an order for cookies") == IntentEnum.create_order
    assert detect_intent("recommend me something") == IntentEnum.recommend_products
    assert detect_intent("hello") == IntentEnum.greeting

def test_extract_order_details():
    mock_db = MagicMock()
    mock_product = Product(id=1, name="Chocolate Cake", price=10.0)
    mock_db.query.return_value.all.return_value = [mock_product]
    
    product, quantity = extract_order_details("I want 2 Chocolate Cake", mock_db)
    assert product.name == "Chocolate Cake"
    assert quantity == 2
    
    product, quantity = extract_order_details("I want a Chocolate Cake", mock_db)
    assert product.name == "Chocolate Cake"
    assert quantity == 1

def test_extract_customer_details():
    name, email, phone = extract_customer_details("My name is John, email is john@example.com, phone 1234567890")
    assert email == "john@example.com"
    assert phone == "1234567890"
    # Name extraction is basic, might fail or be partial, let's check if it got something
    assert name == "John"

    name, email, phone = extract_customer_details("john@example.com")
    assert email == "john@example.com"

@patch("app.api.v1.assistant.send_order_confirmation_email")
def test_chat_create_order_flow(mock_send_email):
    mock_db = MagicMock()
    mock_product = Product(id=1, name="Chocolate Cake", price=10.0)
    mock_db.query.return_value.all.return_value = [mock_product]
    # Mock query for product by id (used in order creation if any, but here we use object directly or mock query)
    # The code uses db.add, db.commit. We should mock those.
    
    # 1. User asks to order
    req = ChatRequest(messages=[ChatMessage(role="user", content="I want to order a Chocolate Cake")])
    resp = chat(req, db=mock_db)
    print(f"DEBUG: Reply 1: {resp.reply.text}")
    assert resp.reply.intent == IntentEnum.create_order
    assert "Name, Email, and Phone" in resp.reply.text
    
    # 2. User provides details
    # We need to simulate history
    req = ChatRequest(messages=[
        ChatMessage(role="user", content="I want to order a Chocolate Cake"),
        ChatMessage(role="assistant", content=resp.reply.text),
        ChatMessage(role="user", content="John Doe, john@example.com, 1234567890")
    ])
    
    # We need to ensure extract_order_details finds the product from history
    # The code looks at history_text.
    
    resp = chat(req, db=mock_db)
    print(f"DEBUG: Reply 2: {resp.reply.text}")
    assert resp.reply.intent == IntentEnum.create_order
    assert "placed successfully" in resp.reply.text
    
    # Verify DB calls
    assert mock_db.add.call_count >= 2 # Order and OrderItem
    mock_db.commit.assert_called()
    
    # Verify Email call
    mock_send_email.assert_called_once()
    args, _ = mock_send_email.call_args
    assert args[0] == "john@example.com"
    assert args[1]["total_amount"] == 10.0
