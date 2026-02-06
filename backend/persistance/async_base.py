
"""Centralized async SQLAlchemy engine and session factory.

This module exposes a single async engine and an `AsyncSession` factory
that the rest of the codebase should import. It also provides a typed
FastAPI dependency `get_async_session` that yields an `AsyncSession`.
"""

from typing import AsyncGenerator
import os

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool
from backend.config import settings

# Normalize DB URL to an async driver if necessary
db_url = settings.DATABASE_URL
# In test runs prefer an in-memory SQLite DB unless explicitly overridden.
if settings.ENV == "test":
    db_url = os.environ.get("TEST_DATABASE_URL", "sqlite+aiosqlite:///:memory:")
elif db_url.startswith("postgresql+psycopg2"):
    db_url = db_url.replace("postgresql+psycopg2", "postgresql+asyncpg")

# Single async engine for the application
if "postgresql+asyncpg" in db_url:
    # Postgres (asyncpg): configure a small pool to avoid reusing a single
    # connection across concurrent coroutines which can trigger asyncpg
    # "another operation is in progress" errors.
    async_engine: AsyncEngine = create_async_engine(
        db_url,
        echo=False,
        future=True,
        pool_size=5,
        max_overflow=10,
    )
elif db_url.startswith("sqlite"):
    # In-memory sqlite (aiosqlite) must use StaticPool and appropriate
    # connect args so the same DB is available across connections in tests.
    async_engine: AsyncEngine = create_async_engine(
        db_url,
        echo=False,
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    # Fallback: create engine without special pooling parameters
    async_engine: AsyncEngine = create_async_engine(db_url, echo=False, future=True)

# Async session factory (SQLAlchemy 2.0 style)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an `AsyncSession`.

    Usage:
        async def endpoint(session: AsyncSession = Depends(get_async_session)):
            ...
    """
    async with AsyncSessionLocal() as session:
        yield session


# Backwards-compatible export for scripts that import `async_sessionmaker`
async_sessionmaker = AsyncSessionLocal

# Backwards-compatible alias for code/tests expecting `engine`
engine = async_engine







