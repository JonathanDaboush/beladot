import os
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from main import app, Base, get_db
import asyncio

# 3. Use test DB URL (matches docker-compose)
os.environ["TESTING"] = "1"
DB_USER = "appuser"
DB_PASS = "password"
DB_HOST = "localhost"
DB_NAME = "app_test"
DB_PORT = 5433
TEST_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine_test = create_async_engine(TEST_DATABASE_URL, echo=True)
AsyncSessionTest = async_sessionmaker(engine_test, expire_on_commit=False)

@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine_test.dispose()

# 7. Override get_db for tests to use test DB
async def override_get_db():
    async with AsyncSessionTest() as session:
        yield session
app.dependency_overrides[get_db] = override_get_db

import httpx
from httpx import ASGITransport

@pytest.mark.asyncio
async def test_create_item():
    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/items", json={"name": "TestItem"})
        assert response.status_code == 200
        assert response.json()["name"] == "TestItem"

# 8. Comments:
# - Test DB runs on port 5433, dev DB on 5432, so tests never touch dev data.
# - Each test gets a fresh async session, avoiding InterfaceError.
# - Table creation in setup_db prevents 500 errors from missing tables.
