import os
import logging
from typing import Optional

from supabase import create_client, Client

logger = logging.getLogger(__name__)


class SupabaseSettings:
    def __init__(self) -> None:
        self.url: Optional[str] = os.getenv("SUPABASE_URL")
        self.service_key: Optional[str] = os.getenv("SUPABASE_SERVICE_KEY")


_settings = SupabaseSettings()
_client: Optional[Client] = None


def get_client() -> Client:
    """Return a singleton Supabase client using server-side service key.

    Requires env vars: SUPABASE_URL, SUPABASE_SERVICE_KEY
    """
    global _client
    if _client is not None:
        return _client

    if not _settings.url or not _settings.service_key:
        raise RuntimeError(
            "Supabase not configured. Set SUPABASE_URL and SUPABASE_SERVICE_KEY in .env"
        )

    _client = create_client(_settings.url, _settings.service_key)
    logger.info("Supabase client initialized for URL: %s", _settings.url)
    return _client
