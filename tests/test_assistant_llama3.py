import pytest
from unittest.mock import MagicMock, patch
from app.api.v1.assistant import chat
from app.schemas.assistant import IntentEnum, ChatRequest, ChatMessage
# SQLAlchemy models removed; using Supabase now
import json

@patch("app.api.v1.assistant.client")
@patch("app.api.v1.assistant.send_order_confirmation_email")
def test_chat_llama3_flow(mock_send_email, mock_groq):
    mock_db = MagicMock()
    mock_product = Product(id=1, name="Chocolate Cake", price=10.0)
    mock_db.query.return_value.all.return_value = [mock_product]
    mock_db.query.return_value.filter.return_value.first.return_value = mock_product
    
    # Mock Groq Response for Order Creation
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = json.dumps({
        "intent": "create_order",
        "reply_text": "Order placed!",
        "order_details": {
            "product_id": 1,
            "quantity": 2,
            "customer_name": "Alice",
            "customer_email": "alice@test.com",
            "customer_phone": "555-1234"
        },
        "missing_info": []
    })
    mock_groq.chat.completions.create.return_value = mock_completion
    
    # Test Request
    req = ChatRequest(messages=[ChatMessage(role="user", content="I want 2 Chocolate Cakes. Name is Alice, alice@test.com, 555-1234")])
    resp = chat(req, db=mock_db)
    
    # Assertions
    assert resp.reply.intent == IntentEnum.create_order
    assert resp.reply.text == "Order placed!"
    
    # Verify DB calls
    assert mock_db.add.call_count >= 2
    mock_db.commit.assert_called()
    
    # Verify Email
    mock_send_email.assert_called_once()
    args, _ = mock_send_email.call_args
    assert args[0] == "alice@test.com"
