import os
import sys
import asyncio
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
os.environ.setdefault(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./test.db"
)

# ---------------------------------------------------------------
# Imports AFTER env setup
# ---------------------------------------------------------------
from fastapi.testclient import TestClient
from backend.app import app, get_db
from backend.persistance.async_base import AsyncSessionLocal, engine
from backend.persistance.base import Base

# ---------------------------------------------------------------
# Override get_db dependency (ASYNC + MANAGED)
# ---------------------------------------------------------------
async def override_get_db():
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
# Database cleanup after all tests
# ---------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
async def cleanup_db():
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
