
from fastapi.testclient import TestClient
import sys
import os
import pytest
# Ensure backend is importable when running from project root
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)

# -------------------------------------------------------------------
# FIXTURE: FastAPI client (DELAYED app import)
# -------------------------------------------------------------------
@pytest.fixture(scope="function")
def setup_test_database():
    # Tests already use the session-scoped conftest.py init_db fixture
    # which creates all tables via Base.metadata.create_all()
    # This fixture now just yields without doing anything since the DB is already set up
    yield
    
    
@pytest.fixture(scope="session")
def client():
    from backend.app import app
    return TestClient(app)


# -------------------------------------------------------------------
# (No extra duplicate fixtures)
# -------------------------------------------------------------------


# -------------------------------------------------------------------
# BASIC API TESTS
# -------------------------------------------------------------------

def test_api_finance_issues_catalog(client: TestClient):
    response = client.get("/api/finance/issues")
    assert response.status_code in (200, 401)


def test_api_finance_create_issue_missing_fields(client: TestClient):
    response = client.post("/api/finance/issues", json={})
    assert response.status_code in (400, 401)
    assert "detail" in response.json()


def test_api_employee_components_for_employee_forbidden(client: TestClient):
    response = client.get("/api/employee_components/for_employee")
    assert response.status_code in (401, 403)


def test_api_get_cart_items(client: TestClient):
    response = client.get("/api/get_cart_items")
    assert response.status_code in (200, 401)


def test_api_add_item_to_cart_missing(client: TestClient):
    response = client.post("/api/add_item_to_cart", json={})
    assert response.status_code in (400, 401)


# -------------------------------------------------------------------
# DATABASE-DEPENDENT TESTS
# -------------------------------------------------------------------

def test_api_manager_edit_employee_info(
    setup_test_database: object, client: TestClient, monkeypatch: pytest.MonkeyPatch
):
    import asyncio
    from backend.persistance.async_base import AsyncSessionLocal
    from backend.persistance.department import Department
    from backend.persistance.user import User
    from backend.persistance.manager import Manager
    from backend.persistance.employee import Employee
    from backend.persistance.shift import Shift
    import datetime as dt

    async def _seed():
        async with AsyncSessionLocal() as db:
            db.add(Department(department_id=1, name="Test Department"))

            db.add_all([
                User(
                    user_id=1,
                    full_name="Manager User",
                    dob=dt.date(1990, 1, 1),
                    password="pass",
                    phone_number="123",
                    email="manager@example.com",
                    created_at=dt.date.today(),
                    img_location="",
                    account_status="True",
                ),
                User(
                    user_id=2,
                    full_name="Employee User",
                    dob=dt.date(1992, 2, 2),
                    password="pass",
                    phone_number="456",
                    email="employee@example.com",
                    created_at=dt.date.today(),
                    img_location="",
                    account_status="True",
                ),
            ])

            db.add_all([
                Manager(
                    manager_id=1,
                    user_id=1,
                    department_id=1,
                    is_active=True,
                    created_at=dt.datetime.now(),
                    last_active_at=dt.datetime.now(),
                ),
                Employee(emp_id=1, user_id=2, department_id=1),
            ])

            from backend.persistance.enums import ShiftStatusEnum
            db.add(
                Shift(
                    shift_id=1,
                    emp_id=1,
                    start_time=dt.datetime.now(),
                    end_time=dt.datetime.now() + dt.timedelta(hours=8),
                    created_by_manager_id=1,
                    status=ShiftStatusEnum.scheduled,
                )
            )

            await db.commit()

    asyncio.run(_seed())

    import backend.services.managerServices as manager_services
    monkeypatch.setattr(
        manager_services,
        "get_current_user",
        lambda: {"manager_id": 1},
        raising=False,
    )

    response = client.put(
        "/api/v1/manager/employee/1",
        json={"notes": "Test update"},
        headers={"Authorization": "Bearer testtoken"} # Add auth if needed
    )

    assert response.status_code in (200, 401)


def test_api_employee_book_shift(setup_test_database: object, client: TestClient):
    import asyncio
    from backend.persistance.async_base import AsyncSessionLocal
    from backend.persistance.shift import Shift
    from backend.persistance.department import Department
    from backend.persistance.user import User
    from backend.persistance.manager import Manager
    from backend.persistance.employee import Employee
    from backend.persistance.enums import ShiftStatusEnum
    from sqlalchemy import select
    import datetime as dt

    async def _seed():
        async with AsyncSessionLocal() as db:
            # Setup test data
            db.add(Department(department_id=1, name="Test Department"))
            db.add_all([
                User(
                    user_id=1,
                    full_name="Manager User",
                    dob=dt.date(1990, 1, 1),
                    password="pass",
                    phone_number="123",
                    email="manager2@example.com",
                    created_at=dt.date.today(),
                    img_location="",
                    account_status="True",
                ),
                User(
                    user_id=2,
                    full_name="Employee User",
                    dob=dt.date(1992, 2, 2),
                    password="pass",
                    phone_number="456",
                    email="employee2@example.com",
                    created_at=dt.date.today(),
                    img_location="",
                    account_status="True",
                ),
            ])
            db.add_all([
                Manager(
                    manager_id=1,
                    user_id=1,
                    department_id=1,
                    is_active=True,
                    created_at=dt.datetime.now(),
                    last_active_at=dt.datetime.now(),
                ),
                Employee(emp_id=2, user_id=2, department_id=1),
            ])
            db.add(Shift(
                shift_id=100,
                emp_id=2,
                start_time=dt.datetime.now(),
                end_time=dt.datetime.now() + dt.timedelta(hours=8),
                created_by_manager_id=1,
                status=ShiftStatusEnum.scheduled,
            ))
            await db.commit()
            
            result = await db.execute(select(Shift).order_by(Shift.shift_id.desc()))
            shift = result.scalars().first()
            return shift

    shift = asyncio.run(_seed())

    assert shift is not None

    response = client.post(
        "/api/book_shift",
        json={"employee_id": 1, "shift_id": shift.shift_id},
    )

    assert response.status_code in (200, 401)


# -------------------------------------------------------------------
# INTEGRATION TEST
# -------------------------------------------------------------------

@pytest.mark.integration
def test_upload_image(tmp_path: object, client: TestClient):
    from pathlib import Path
    file_path = Path(str(tmp_path)) / "test.jpg"
    file_path.write_bytes(b"test image")

    with open(file_path, "rb") as f:
        response = client.post(
            "/api/v1/uploads/images",
            files={"file": ("test.jpg", f, "image/jpeg")},
        )

    assert response.status_code == 200
    data = response.json()
    assert "image_url" in data
    assert "image_id" in data



 
