import pytest
from backend.app import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_readiness():
    response = client.get("/readiness")
    assert response.status_code in (200, 503)

def test_rate_limit():
    for _ in range(101):
        response = client.get("/health")
    assert response.status_code in (200, 429)

def test_transaction_rollback():
    from backend.repositories.repository.user_repository import UserRepository
    from backend.persistance.user import User
    from backend.persistance.async_base import AsyncSessionLocal
    import pytest
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
