import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
from main import app, Base, get_db
import asyncio

# Use a separate test DB (adjust as needed)
TEST_DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/test_db"
engine_test = create_async_engine(TEST_DATABASE_URL, echo=True, poolclass=NullPool)
AsyncSessionTest = async_sessionmaker(engine_test, expire_on_commit=False)

@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine_test.dispose()

# Override get_db for tests to use test DB
async def override_get_db():
    async with AsyncSessionTest() as session:
        yield session
app.dependency_overrides[get_db] = override_get_db

@pytest.mark.asyncio
async def test_create_item():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/items", json={"name": "TestItem"})
        assert response.status_code == 200
        assert response.json()["name"] == "TestItem"
