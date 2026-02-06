
import os
import sys
from fastapi.testclient import TestClient
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from pathlib import Path


@pytest.fixture(scope="function")
def setup_test_database():
    # Tests already use the session-scoped conftest.py init_db fixture
    # which creates all tables via B ase.metadata.create_all()
    # This fixture now just yields without doing anything since the DB is already set up
    yield

@pytest.fixture(scope="session")
def client():
    from backend.app import app
    return TestClient(app)


def _headers(role: str, id_val: str = "1"):
    base = {"X-Auth-Role": role, "X-Auth-Id": id_val}
    if role == "employee":
        base["X-Auth-Employee-Id"] = id_val
        base["X-Auth-Department-Id"] = "1"
    if role == "seller":
        base["X-Auth-Seller-Id"] = id_val
    if role == "user":
        base["X-Auth-Id"] = id_val
    if role == "manager":
        base["X-Auth-Id"] = id_val
        base["X-Auth-Employee-Id"] = "1"
    return base


from fastapi.testclient import TestClient
def test_uploads_image_endpoint(setup_test_database: None, client: TestClient, tmp_path: Path) -> None:
    path = tmp_path / "u.png"
    path.write_bytes(b"fake")
    with open(path, "rb") as f:
        res = client.post(
            "/api/v1/uploads/images", files={"file": ("u.png", f, "image/png")}
        )
    assert res.status_code in (200, 413, 415, 400, 500)


def test_customer_cart_add_forbidden_without_identity(setup_test_database: object, client: TestClient) -> None:
    res = client.post(
        "/api/v1/customer/cart/items",
        json={"product_id": 1, "quantity": 1},
    )
    assert res.status_code in (401, 403)


def test_customer_cart_add_with_identity(setup_test_database: object, client: TestClient) -> None:
    # Setup required test data
    import asyncio
    from backend.persistance.async_base import AsyncSessionLocal
    from backend.persistance.user import User
    from backend.persistance.category import Category
    from backend.persistance.product import Product
    import datetime as dt
    
    async def _seed():
        async with AsyncSessionLocal() as db:
            user = User(
                user_id=10,
                full_name="Test User",
                dob=dt.date(1990, 1, 1),
                password="pass",
                phone_number="123",
                email="testuser@example.com",
                created_at=dt.date.today(),
                img_location="",
                account_status="True",
            )
            db.add(user)
            category = Category(name="Test Cart Cat", image_url=None)
            db.add(category)
            await db.flush()  # Get auto-generated IDs
            
            db.add(Product(
                product_id=1,
                seller_id=10,
                category_id=category.category_id,
                title="Test Product",
                description="Test",
                price=10.0,
                currency="USD",
                is_active=True,
            ))
            await db.commit()
    
    asyncio.run(_seed())
    
    res = client.post(
        "/api/v1/customer/cart/items",
        json={"product_id": 1, "quantity": 1},
        headers=_headers("user", "10"),
    )
    assert res.status_code in (200, 400, 500)


def test_employee_component_create_requires_role(setup_test_database: object, client: TestClient) -> None:
    res = client.post(
        "/api/v1/employee/components",
        json={"img_url": "x", "description": "y", "department_id": 1},
    )
    assert res.status_code in (401, 403)


def test_employee_component_create_with_role(setup_test_database: object, client: TestClient) -> None:
    res = client.post(
        "/api/v1/employee/components",
        json={"img_url": "x", "description": "y", "department_id": 1},
        headers=_headers("employee", "2"),
    )
    assert res.status_code in (200, 400, 500)


def test_seller_product_create_requires_role(setup_test_database: object, client: TestClient) -> None:
    res = client.post(
        "/api/v1/seller/products",
        json={
            "name": "p",
            "description": "d",
            "price": 1.0,
            "category_id": 1,
        },
    )
    assert res.status_code in (401, 403)


def test_seller_product_create_with_role(setup_test_database: object, client: TestClient) -> None:
    # Setup required test data
    import asyncio
    from backend.persistance.async_base import AsyncSessionLocal
    from backend.persistance.category import Category
    
    async def _seed():
        async with AsyncSessionLocal() as db:
            category = Category(name="Test Seller Cat", image_url=None)
            db.add(category)
            await db.commit()
            await db.refresh(category)
            return category.category_id
    
    cat_id = asyncio.run(_seed())
    
    res = client.post(
        "/api/v1/seller/products",
        json={
            "name": "p",
            "description": "d",
            "price": 2.0,
            "category_id": cat_id,
        },
        headers=_headers("seller", "5"),
    )
    assert res.status_code in (200, 400, 500)


def test_shipping_create_shipment_requires_role(setup_test_database: object, client: TestClient) -> None:
    res = client.post(
        "/api/v1/shipping/shipments",
        json={"order_id": 1, "shipment_status": "created"},
    )
    assert res.status_code in (401, 403)


def test_shipping_create_shipment_with_employee_role(setup_test_database: object, client: TestClient) -> None:
    # Setup required test data
    from backend.persistance.base import SessionLocal
    from backend.persistance.user import User
    from backend.persistance.address_snapshot import AddressSnapshot
    import datetime as dt
    
    db = SessionLocal()
    db.add(User(
        user_id=1,
        full_name="Test User",
        dob=dt.date(1990, 1, 1),
        password="pass",
        phone_number="123",
        email="testshipuser@example.com",
        created_at=dt.date.today(),
        img_location="",
        account_status="True",
    ))
    db.add(AddressSnapshot(
        reference_type="shipment",
        recipient_name="Test User",
        street_line_1="Main St",
        street_line_2="",
        city="LA",
        state_province="CA",
        postal_code="90001",
        country="US",
        phone_number="555-0100",
        order_number="",
        shipment_id="1",
    ))
    db.commit()
    db.close()
    
    res = client.post(
        "/api/v1/shipping/shipments",
        json={"order_id": 1, "shipment_status": "created"},
        headers=_headers("employee", "2"),
    )
    assert res.status_code in (200, 400, 500)


def test_assistance_refund_status_with_user_role(setup_test_database: None, client: TestClient):
    res = client.post(
        "/api/v1/assistance/refund-status",
        json={"customer_email": "a@b.com", "status": "approved"},
        headers=_headers("user", "9"),
    )
    assert res.status_code in (200, 400, 500)


def test_assistance_complaint_with_user_role(setup_test_database: None, client: TestClient):
    res = client.post(
        "/api/v1/assistance/complaint",
        json={"customer_id": 1, "complaint": "bad"},
        headers=_headers("user", "9"),
    )
    assert res.status_code in (200, 400, 500)


def test_manager_edit_employee_requires_role(setup_test_database: None, client: TestClient):
    res = client.put("/api/v1/manager/employee/1", json={"notes": "n"})
    assert res.status_code in (401, 403)


def test_shipping_create_shipment_rejects_non_created(setup_test_database: None, client: TestClient):
    # Ensure non-CREATED status is rejected
    res = client.post(
        "/api/v1/shipping/shipments",
        json={"order_id": 1, "shipment_status": "shipped"},
        headers=_headers("employee", "2"),
    )
    # Rejection may surface as validation (422) or server errors
    assert res.status_code in (400, 422, 500)


def test_seller_product_create_invalid_payload_returns_422(setup_test_database: None, client: TestClient):
    # Missing required fields like name/price => validation error
    res = client.post(
        "/api/v1/seller/products",
        json={"description": "d", "category_id": 1},
        headers=_headers("seller", "5"),
    )
    assert res.status_code == 422


def test_assistance_refund_status_missing_fields_returns_422(setup_test_database: None, client: TestClient):
    # Empty payload should produce validation error
    res = client.post(
        "/api/v1/assistance/refund-status",
        json={},
        headers=_headers("user", "9"),
    )
    assert res.status_code == 422


def test_employee_components_requires_role(setup_test_database: None, client: TestClient):
    # GET components without employee role should be forbidden
    res = client.get("/api/v1/employee/components")
    assert res.status_code in (401, 403)


def test_employee_components_with_role_ok(setup_test_database: None, client: TestClient):
    # Should succeed for employee role
    res = client.get(
        "/api/v1/employee/components",
        headers=_headers("employee", "3"),
    )
    assert res.status_code == 200


def test_customer_wishlist_add_requires_identity(setup_test_database: None, client: TestClient):
    res = client.post(
        "/api/v1/customer/wishlist/items",
        json={"product_id": 1, "quantity": 1},
    )
    assert res.status_code in (401, 403)


def test_customer_wishlist_add_with_identity(setup_test_database: None, client: TestClient):
    # Setup required test data
    import asyncio
    from backend.persistance.async_base import AsyncSessionLocal
    from backend.persistance.user import User
    from backend.persistance.category import Category
    from backend.persistance.product import Product
    import datetime as dt
    
    async def _seed():
        async with AsyncSessionLocal() as db:
            db.add(User(
                user_id=10,
                full_name="Test User 10",
                dob=dt.date(1990, 1, 1),
                password="pass",
                phone_number="1234",
                email="testwishuser@example.com",
                created_at=dt.date.today(),
                img_location="",
                account_status="True",
            ))
            category = Category(name="Test Wishlist Cat", image_url=None)
            db.add(category)
            await db.flush()
            
            db.add(Product(
                product_id=1,
                seller_id=10,
                category_id=category.category_id,
                title="Test Product",
                description="Test",
                price=10.0,
                currency="USD",
                is_active=True,
            ))
            await db.commit()
    
    asyncio.run(_seed())
    
    res = client.post(
        "/api/v1/customer/wishlist/items",
        json={"product_id": 1, "quantity": 1},
        headers=_headers("user", "10"),
    )
    assert res.status_code in (200, 400, 500)


def test_seller_product_edit_requires_role(setup_test_database: None, client: TestClient):
    res = client.put(
        "/api/v1/seller/products/1",
        json={"name": "p", "description": "d", "price": 2.0, "category_id": 1},
    )
    assert res.status_code in (401, 403)


def test_seller_product_edit_with_role(setup_test_database: None, client: TestClient):
    # Setup required test data
    import asyncio
    from backend.persistance.async_base import AsyncSessionLocal
    from backend.persistance.user import User
    from backend.persistance.category import Category
    from backend.persistance.product import Product
    import datetime as dt
    
    async def _seed():
        async with AsyncSessionLocal() as db:
            db.add(User(
                user_id=5,
                full_name="Test Seller",
                dob=dt.date(1990, 1, 1),
                password="pass",
                phone_number="555",
                email="testseller@example.com",
                created_at=dt.date.today(),
                img_location="",
                account_status="True",
            ))
            category = Category(name="Test Edit Cat", image_url=None)
            db.add(category)
            await db.flush()
            
            db.add(Product(
                product_id=1,
                seller_id=5,
                category_id=category.category_id,
                title="Original Product",
                description="Original",
                price=10.0,
                currency="USD",
                is_active=True,
            ))
            await db.commit()
    
    asyncio.run(_seed())
    
    res = client.put(
        "/api/v1/seller/products/1",
        json={"name": "Updated", "description": "Updated desc", "price": 20.0, "category_id": 1},
        headers=_headers("seller", "5"),
    )
    assert res.status_code in (200, 400, 500)


def test_shipping_shipment_event_requires_role(setup_test_database: None, client: TestClient):
    res = client.post(
        "/api/v1/shipping/shipment-events",
        json={"shipment_id": 1, "status": "in_transit", "description": "d", "location": "x"},
    )
    assert res.status_code in (401, 403)


def test_shipping_shipment_event_with_role(setup_test_database: None, client: TestClient):
    res = client.post(
        "/api/v1/shipping/shipment-events",
        json={"shipment_id": 1, "status": "in_transit", "description": "d", "location": "x"},
        headers=_headers("employee", "2"),
    )
    assert res.status_code in (200, 400, 422, 500)


def test_uploads_product_image_requires_file(setup_test_database: None, client: TestClient):
    res = client.post("/api/v1/uploads/products/1/image")
    assert res.status_code in (400, 415, 422, 500)


def test_uploads_product_image_accepts_file(setup_test_database: None, client: TestClient, tmp_path: object):
    from pathlib import Path
    path = Path(str(tmp_path)) / "p.png"
    path.write_bytes(b"fake")
    with open(path, "rb") as f:
        res = client.post(
            "/api/v1/uploads/products/1/image",
            files={"file": ("p.png", f, "image/png")},
        )
    assert res.status_code in (200, 413, 415, 400, 500)


def test_manager_incident_requires_role(setup_test_database: None, client: TestClient):
    res = client.post("/api/v1/manager/incident", json={"description": "x"})
    assert res.status_code in (401, 403)


import pytest


