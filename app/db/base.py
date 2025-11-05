"""Base class for SQLAlchemy models."""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models here to ensure they are registered with Base.metadata
# This is important for Alembic migrations
from app.models import product, order  # noqa
