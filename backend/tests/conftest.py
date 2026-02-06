import os
import sys
## Removed duplicate import
import pytest

# ---------------------------------------------------------------
# Ensure backend is importable from project root
# ---------------------------------------------------------------
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)

# ---------------------------------------------------------------
# Set test database URL BEFORE importing backend
# ---------------------------------------------------------------
# Default test database to in-memory SQLite to avoid local Postgres auth
# issues during CI/dev runs. Override by setting `DATABASE_URL` in the
# environment if Postgres is available and desired.
# Force tests to use a local in-memory DB unless `TEST_DATABASE_URL` is set.
# This ensures CI/dev runs don't attempt to use a local Postgres instance
# with potentially mismatched credentials.
sqlite_url = os.environ.get("TEST_DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ["IGNORE_DATABASE_URL"] = sqlite_url
os.environ.setdefault("TEST_DATABASE_URL", sqlite_url)

# Ensure environment is set for settings loading
os.environ["ENV"] = "test"
os.environ.setdefault("EMAIL_API_KEY", "test-email-key")
os.environ.setdefault("SECRET_KEY", "change-me")

# ---------------------------------------------------------------
# Imports AFTER env setup
# ---------------------------------------------------------------
from fastapi.testclient import TestClient
from backend.app import app, get_db
from backend.persistance.async_base import AsyncSessionLocal, engine
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from backend.persistance.base import Base

# ---------------------------------------------------------------
# Override get_db dependency (ASYNC + MANAGED)
# ---------------------------------------------------------------
async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

@pytest.fixture(scope="session", autouse=True)
def override_db_dependency():
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()

# ---------------------------------------------------------------
# FastAPI test client
# ---------------------------------------------------------------
@pytest.fixture(scope="session")
def client():
    return TestClient(app)

# ---------------------------------------------------------------
# Event loop (required on Windows)
# ---------------------------------------------------------------
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

# ---------------------------------------------------------------
# Reset database schema before tests (drop -> create)
# ---------------------------------------------------------------
import asyncio
@pytest.fixture(scope="session", autouse=True)
def init_db(event_loop: asyncio.AbstractEventLoop):
    # Import all persistence models to populate Base.metadata
    import backend.persistance  # This triggers all model imports in __init__.py

    async def _setup():
        async with engine.begin() as conn:
            def drop_all_sqlite_tables(connection):
                # Get all table names
                from sqlalchemy import inspect
                inspector = inspect(connection)
                tables = inspector.get_table_names()
                
                # Disable foreign key constraints temporarily
                connection.execute(text("PRAGMA foreign_keys = OFF"))
                
                # Drop each table
                for table in tables:
                    connection.execute(text(f'DROP TABLE IF EXISTS "{table}"'))
                
                # Re-enable foreign key constraints
                connection.execute(text("PRAGMA foreign_keys = ON"))

            # Import text for raw SQL
            from sqlalchemy import text
            
            # Drop all tables using SQLite-specific approach for clean slate
            if "sqlite" in str(conn.dialect.name).lower():
                await conn.run_sync(drop_all_sqlite_tables)
            else:
                # For other databases, use metadata drop_all
                await conn.run_sync(Base.metadata.drop_all)
            
            # Recreate schema to ensure all tables exist before tests
            await conn.run_sync(Base.metadata.create_all)

    event_loop.run_until_complete(_setup())
    # Tests run after this yield; final cleanup handled below
    yield

# ---------------------------------------------------------------
# Database cleanup after all tests
# ---------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def cleanup_db(event_loop: asyncio.AbstractEventLoop):
    yield
    async def _cleanup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    event_loop.run_until_complete(_cleanup())
