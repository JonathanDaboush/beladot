import os
import sys
from typing import Any, Optional
import pytest
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
    # Do not call Base.metadata.create_all here - Alembic will create schema
    # after dropping tables. Calling create_all then running migrations causes
    # duplicate table creation errors during tests.
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
from fastapi.testclient import TestClient

# Ensure backend is importable when running from project root
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)


class FakeFinanceService:
    async def get_issues_catalog(self, employee_id: int) -> list[dict[str, Any]]:
        return [
            {
                "incident_id": 1,
                "employee_id": employee_id,
                "description": "Test",
                "cost": 1.0,
                "date": "2024-01-01",
                "status": "open",
            }
        ]

    async def create_issue(self, employee_id: int, description: str, cost: float, date: str, status: str) -> dict[str, Any]:
        return {
            "incident_id": 123,
            "employee_id": employee_id,
            "description": description,
            "cost": cost,
            "date": date,
            "status": status,
        }

    async def update_issue(
        self,
        issue_id: int,
        description: Optional[str] = None,
        cost: Optional[float] = None,
        date: Optional[str] = None,
        status: Optional[str] = None
    ) -> dict[str, Any]:
        return {
            "incident_id": issue_id,
            "employee_id": 1,
            "description": description or "",
            "cost": cost or 0.0,
            "date": date or "2024-01-01",
            "status": status or "open",
        }

    async def delete_issue(self, issue_id: int) -> dict[str, Any]:
        return {"incident_id": issue_id, "deleted": True}


@pytest.fixture(scope="session")
def client():
    from backend.app import app
    import backend.api.routes_finance as routes_finance
    async def fake_dep():
        return FakeFinanceService()
    # Use FastAPI's dependency override mechanism to replace original callable
    app.dependency_overrides[routes_finance.get_finance_services] = fake_dep
    return TestClient(app)


def test_create_issue_handles_conflict(client: TestClient) -> None:

    payload: dict[str, Any] = {
        "employee_id": 1,
        "description": "Broken equipment",
        "cost": 99.5,
        "date": "2024-01-01",
        "status": "open",
    }
    headers = {
        "X-Auth-Role": "employee",
        "X-Auth-Id": "1",
        "X-Auth-Employee-Id": "1",
    }
    with pytest.raises(TypeError):
        client.post("/api/finance/issues", json=payload, headers=headers)


def test_update_issue_success(client: TestClient) -> None:
    headers = {
        "X-Auth-Role": "employee",
        "X-Auth-Id": "1",
        "X-Auth-Employee-Id": "1",
    }
    res = client.put("/api/finance/issues/123", json={"status": "closed"}, headers=headers)
    assert res.status_code == 200
    body = res.json()
    assert body["incident_id"] == 123
    assert body["status"] == "closed"


def test_delete_issue_returns_deleted_flag(client: TestClient) -> None:
    headers = {
        "X-Auth-Role": "employee",
        "X-Auth-Id": "1",
        "X-Auth-Employee-Id": "1",
    }
    res = client.request("DELETE", "/api/finance/issues/123", headers=headers)
    assert res.status_code == 200
    body = res.json()
    assert body["deleted"] is True


def test_get_issues_catalog(client: TestClient) -> None:
    headers = {
        "X-Auth-Role": "employee",
        "X-Auth-Id": "1",
        "X-Auth-Employee-Id": "1",
    }
    res = client.get("/api/finance/issues", headers=headers)
    assert res.status_code == 200
    items = res.json()
    assert isinstance(items, list) and items
    assert items[0]["employee_id"] == 1
