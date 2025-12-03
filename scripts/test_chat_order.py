import httpx
import time
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_order_flow():
    print("🚀 Starting Order Flow Test...")
    
    # 1. Check Health
    try:
        r = httpx.get(f"{BASE_URL}/health")
        if r.status_code != 200:
            print("❌ Server not healthy or not running.")
            return
        print("✅ Server is healthy.")
    except Exception as e:
        print(f"❌ Could not connect to server: {e}")
        return

    # 2. Start Conversation: "I want to order a Chocolate Cake"
    # Note: We need to ensure "Chocolate Cake" exists in DB. 
    # If not, we might need to seed it or use a generic one if seeded.
    # Let's assume the database has some products or we'll fail to find it.
    
    print("\n1️⃣  User: 'I want to order a Chocolate Cake'")
    payload = {
        "messages": [{"role": "user", "content": "I want to order a Chocolate Cake"}],
        "top_n": 5
    }
    r = httpx.post(f"{BASE_URL}/api/v1/assistant/chat", json=payload)
    data = r.json()
    reply = data['reply']['text']
    print(f"🤖 Bot: {reply}")
    
    # Check if bot asks for details
    if "Name" not in reply and "Email" not in reply:
        print("⚠️ Bot didn't ask for details immediately. It might have failed to find the product or logic is different.")
        # Try to provide details anyway in next step
    
    # 3. Provide Details: "John Doe, john@example.com, 1234567890"
    print("\n2️⃣  User: 'John Doe, john@example.com, 1234567890'")
    # We need to send the FULL history for the context to work as per my implementation
    payload["messages"].append({"role": "assistant", "content": reply})
    payload["messages"].append({"role": "user", "content": "John Doe, john@example.com, 1234567890"})
    
    r = httpx.post(f"{BASE_URL}/api/v1/assistant/chat", json=payload)
    data = r.json()
    reply = data['reply']['text']
    print(f"🤖 Bot: {reply}")
    
    if "placed successfully" in reply:
        print("✅ Order placement successful!")
    else:
        print("❌ Order placement failed or bot didn't recognize it.")

if __name__ == "__main__":
    test_order_flow()
