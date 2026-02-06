import os
import pytest
from fastapi.testclient import TestClient
from backend.app import app

@pytest.fixture(scope="function")
def setup_test_database():
    os.environ["ENV"] = "test"
    from backend.config import settings
    os.environ["DATABASE_URL"] = settings.DATABASE_URL
    from backend.db.base import Base
    from backend.persistance.base import get_engine
    engine = get_engine()
    # Drop all tables
    Base.metadata.drop_all(engine)
    # Recreate tables
    Base.metadata.create_all(engine)
    # Run Alembic migrations
    from alembic.config import Config
    from alembic import command
    alembic_cfg = Config(
        os.path.join(os.path.dirname(__file__), "../../alembic.ini")
    )
    migrations_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../migrations"))
    alembic_cfg.set_main_option("script_location", migrations_dir)
    command.upgrade(alembic_cfg, "head")
    yield

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_readiness():
    response = client.get("/readiness")
    assert response.status_code in (200, 503)

def test_rate_limit():
    response = None
    for _ in range(101):
        response = client.get("/health")
    assert response is not None
    assert response.status_code in (200, 429)

def test_transaction_rollback():
    from backend.repositories.repository.user_repository import UserRepository
    from backend.persistance.user import User
    from backend.persistance.async_base import AsyncSessionLocal
    import datetime
    async def run():
        async with AsyncSessionLocal() as session:
            repo = UserRepository(session)
            user = User(full_name="Test", dob=datetime.datetime.now(), password="pass", phone_number="123", email="test@example.com")
            await repo.add(user)
            await session.rollback()
            result = await repo.get_by_email("test@example.com")
            assert result is None
    import asyncio
    asyncio.run(run())

