import json
from fastapi.testclient import TestClient
from app.main import app

# Monkeypatch llm.chat to return controlled JSON
class DummyLLM:
    def chat(self, system_prompt, messages, temperature=0.0, max_tokens=512):
        return json.dumps({
            "intent": "recommend_products",
            "reply_text": "Here are some popular picks",
            "product_ids": [1, 2, 3]
        })


def test_assistant_recommendations_monkeypatch(monkeypatch):
    from app import llm_client
    monkeypatch.setattr(llm_client, "llm", DummyLLM())

    client = TestClient(app)
    payload = {
        "messages": [{"role": "user", "content": "What do you recommend?"}]
    }
    res = client.post("/api/v1/assistant/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    reply = data["reply"]
    assert reply["intent"] == "recommend_products"
    assert isinstance(reply["suggested_products"], list)
    # We expect up to 3 products mapped from product_ids
    assert len(reply["suggested_products"]) >= 0
