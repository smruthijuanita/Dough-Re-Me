from app.llm_client import GroqClient, Settings
import os

def test_url_logic():
    print("--- Testing Default Settings ---")
    s = Settings()
    # GroqClient only accepts api_key, base_url, model
    client = GroqClient(api_key="test", base_url=s.groq_base_url)
    print(f"Base: {s.groq_base_url}")
    # print(f"API: {s.groq_api_url}") # Removed as it doesn't exist in Settings
    print(f"Client URL: {client.base_url}")
    
    print("\n--- Testing Explicit Base URL (v1) ---")
    client = GroqClient(api_key="test", base_url="https://api.groq.com/openai/v1")
    print(f"Client URL: {client.base_url}")

    # print("\n--- Testing Explicit API URL (v1) ---")
    # # This simulates if GROQ_API_URL was set to the base url by mistake
    # client = GroqClient(api_key="test", base_url="https://api.groq.com/openai/v1", api_url="https://api.groq.com/openai/v1")
    # print(f"Client URL: {client.api_url}")

if __name__ == "__main__":
    test_url_logic()
