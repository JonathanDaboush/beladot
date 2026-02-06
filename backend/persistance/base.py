
# ------------------------------------------------------------------------------
# base.py
# ------------------------------------------------------------------------------
# Defines the declarative base class for all SQLAlchemy ORM models in the
# persistence layer. All ORM models should inherit from this Base class.
# ------------------------------------------------------------------------------

from backend.db.base import Base
# Import for model registration side effects (Base.metadata population)
import backend.persistance as _models
from backend.config import settings

# reference imports to satisfy linters/static checkers (side-effect imports)
_ = _models
_ = Base

from typing import Any
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

# Base is provided by backend.db.base (single declarative registry)


def get_engine() -> Engine:
	"""
	Create and return a synchronous SQLAlchemy Engine using the configured DATABASE_URL.
	This defers environment access until runtime, avoiding import-time failures.
	"""
	# Use application settings (imported at module level) to get DATABASE_URL
	_configured_url = settings.DATABASE_URL
	if "+aiosqlite" in _configured_url:
		_sync_url = _configured_url.replace("+aiosqlite", "")
	elif "+asyncpg" in _configured_url:
		_sync_url = _configured_url.replace("+asyncpg", "+psycopg2")
	else:
		_sync_url = _configured_url
	return create_engine(_sync_url)


def get_sessionmaker() -> sessionmaker[Session]:
	"""
	Return a configured sessionmaker bound to the runtime-created Engine.
	"""
	return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())

class _LazySyncEngineProxy:
	"""Attribute proxy to lazily access the synchronous SQLAlchemy Engine.

	Provides an `engine` symbol for compatibility while deferring actual
	engine creation until first attribute access.
	"""
	def __getattr__(self, name: str) -> Any:
		return getattr(get_engine(), name)

# Public symbol expected by some tests (`engine`)
engine = _LazySyncEngineProxy()

class _LazySessionLocal:
	"""Callable proxy that creates the sync session factory on first use.

	Exposes a `SessionLocal` symbol compatible with legacy imports in tests.
	"""
	def __call__(self, *args: Any, **kwargs: Any) -> Session:
		return get_sessionmaker()(*args, **kwargs)

# Public symbol expected by tests (`SessionLocal`)
SessionLocal = _LazySessionLocal()
