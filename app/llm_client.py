# llm_client.py (patched)
import json
import logging
from typing import List, Dict, Any, Optional
from pydantic_settings import BaseSettings
from groq import Groq

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    groq_api_key: Optional[str] = None
    # Host-only default — do NOT include /openai/v1 here
    groq_base_url: str = "https://api.groq.com"
    groq_model: str = "openai/gpt-oss-20b"

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore",
    }

settings = Settings()
if settings.groq_api_key:
    logger.info("LLM client: GROQ_API_KEY loaded from .env")
else:
    logger.warning("LLM client: GROQ_API_KEY missing. Set it in .env at workspace root.")

def sanitize_base_url(url: str) -> str:
    if not url:
        return url
    u = url.rstrip('/')
    # Remove a mistakenly included "/openai/v1" suffix so SDK doesn't double it
    if u.endswith("/openai/v1"):
        u = u[: -len("/openai/v1")]
    return u

class GroqClient:
    def __init__(self,
                 api_key: Optional[str] = settings.groq_api_key,
                 base_url: str = settings.groq_base_url,
                 model: str = settings.groq_model):
        self.api_key = api_key
        # sanitize base_url to ensure it is host-only (no /openai/v1)
        self.base_url = sanitize_base_url(base_url)
        self.model = model
        self.client: Optional[Groq] = None

        logger.info("Configured GROQ base_url (sanitized): %s", self.base_url)

        if self.api_key:
            # Pass sanitized host-only base_url to SDK
            self.client = Groq(api_key=self.api_key, base_url=self.base_url)
            logger.info("Groq SDK client initialized (base_url=%s)", self.base_url)

    def _chat_completion(self, messages: List[Dict[str, str]], temperature: float, max_tokens: int) -> str:
        if not self.client:
            raise RuntimeError("Missing GROQ_API_KEY environment variable")
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            response_format={"type": "json_object"},
            max_tokens=max_tokens
        )
        return completion.choices[0].message.content

    def chat(self, system_prompt: str, messages: List[Dict[str, str]], temperature: float = 0.0, max_tokens: int = 512) -> str:
        msgs = [{"role": "system", "content": system_prompt}] + messages
        return self._chat_completion(msgs, temperature, max_tokens)

# Convenience instance
llm = GroqClient()
