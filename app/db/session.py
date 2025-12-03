"""
Deprecated: Local PostgreSQL SQLAlchemy session.

This project now uses Supabase exclusively.
Import and use `app.db.supabase.get_client()` for all data operations.
"""

from typing import Generator
from sqlalchemy.orm import Session


def get_db() -> Generator[Session, None, None]:
    raise RuntimeError(
        "Local PostgreSQL session is disabled. Use Supabase client via app.db.supabase.get_client()."
    )
