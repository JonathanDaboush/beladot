
# ------------------------------------------------------------------------------
# base.py
# ------------------------------------------------------------------------------
# Defines the declarative base class for all SQLAlchemy ORM models in the
# persistence layer. All ORM models should inherit from this Base class.
# ------------------------------------------------------------------------------

from backend.db.base import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from backend.config import settings

# Derive a synchronous-compatible URL from the configured DATABASE_URL.
# This ensures sync engine does not attempt to use async drivers like aiosqlite/asyncpg.
_configured_url = settings.DATABASE_URL
if "+aiosqlite" in _configured_url:
	_sync_url = _configured_url.replace("+aiosqlite", "")
elif "+asyncpg" in _configured_url:
	_sync_url = _configured_url.replace("+asyncpg", "+psycopg2")
else:
	_sync_url = _configured_url

engine = create_engine(
	_sync_url,
	connect_args={"check_same_thread": False} if _sync_url.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is provided by backend.db.base (single declarative registry)
