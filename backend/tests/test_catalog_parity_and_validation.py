import os
import sys
import pytest
from fastapi.testclient import TestClient
from typing import Any, Generator, Dict
from sqlite3 import Connection

 

# Ensure backend is importable when running from project root
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)


@pytest.fixture(scope="session")
def client() -> TestClient:
    from backend.app import app
    return TestClient(app)


@pytest.fixture(scope="function")
def setup_test_database() -> Generator[None, None, None]:
    # Tests already use the session-scoped conftest.py init_db fixture
    # which creates all tables via Base.metadata.create_all()
    # This fixture now just yields without doing anything since the DB is already set up
    yield


from sqlalchemy import select
from backend.persistance.category import Category

async def seed_product_and_variant() -> int:
    from backend.persistance.async_base import AsyncSessionLocal
    from backend.persistance.product import Product
    from backend.persistance.product_variant import ProductVariant
    from backend.persistance.user import User
    import datetime as dt

    async with AsyncSessionLocal() as db:
        # Ensure a clean state for the fixed variant_id used in tests
        try:
            result = await db.execute(select(ProductVariant).where(ProductVariant.variant_id == 1))
            existing = result.scalars().first()
            if existing:
                await db.delete(existing)
                await db.commit()
        except Exception:
            pass
        # Ensure required FK parents exist
        # Reuse existing seller user if present to avoid unique email collisions
        result = await db.execute(select(User).where(User.email == "seller@example.com"))
        u = result.scalars().first()
        if not u:
            u = User(
                full_name="Seller One",
                dob=dt.date(1980, 1, 1),
                password="x",
                phone_number="0000000000",
                email="seller@example.com",
                created_at=dt.date.today(),
                img_location="",
                account_status="True",
            )
            db.add(u)
            await db.commit()
            await db.refresh(u)

        # Check if category exists, otherwise create it
        result = await db.execute(select(Category).where(Category.name == "General"))
        c = result.scalars().first()
        if not c:
            c = Category(name="General", image_url=None)
            db.add(c)
            await db.commit()
            await db.refresh(c)

        p = Product(
            title="Test Product",
            description="Desc",
            price=9.99,
            currency="USD",
            is_active=True,
            created_at=dt.datetime.now(),
            updated_at=dt.datetime.now(),
            seller_id=u.user_id,
            category_id=c.category_id,
            subcategory_id=None,
        )
        db.add(p)
        await db.commit()
        await db.refresh(p)

        v = ProductVariant(
            variant_id=1,
            product_id=p.product_id,
            variant_name="Red",
            price=12.34,
            quantity=2,
            is_active=True,
        )
        db.add(v)
        # Also add an inactive product to test invalid case
        p_inactive = Product(
            title="Inactive",
            description="Inactive product description",
            price=5.00,
            currency="USD",
            is_active=False,
            created_at=dt.datetime.now(),
            updated_at=dt.datetime.now(),
            seller_id=u.user_id,
            category_id=1,
            subcategory_id=None,
        )
        db.add(p_inactive)
        await db.commit()
        pid: int = p.product_id
    return pid


def headers_user() -> Dict[str, str]:
    return {
        "X-Auth-Role": "user",
        "X-Auth-Id": "1",
    }


def test_browse_parity_list(setup_test_database: None, client: TestClient) -> None:
    # Seed at least one product
    import asyncio
    async def _seed():
        await seed_product_and_variant()
    asyncio.run(_seed())
    r_guest = client.get("/api/v1/catalog/products")
    r_user = client.get("/api/v1/catalog/products", headers=headers_user())
    assert r_guest.status_code == 200
    assert r_user.status_code == 200
    assert r_guest.json() == r_user.json()


def test_browse_parity_detail(setup_test_database: None, client: TestClient) -> None:
    import asyncio
    async def _seed():
        return await seed_product_and_variant()
    pid: int = asyncio.run(_seed())
    r_guest = client.get(f"/api/v1/catalog/products/{pid}")
    r_user = client.get(f"/api/v1/catalog/products/{pid}", headers=headers_user())
    assert r_guest.status_code == 200
    assert r_user.status_code == 200
    assert r_guest.json() == r_user.json()


def test_validate_cart_public_and_auth(setup_test_database: None, client: TestClient) -> None:
    import asyncio
    async def _seed():
        return await seed_product_and_variant()
    pid: int = asyncio.run(_seed())
    # Guest validation
    payload: Dict[str, Any] = {
        "items": [
            {"product_id": pid, "quantity": 3},  # non-variant
            {"product_id": pid, "variant_id": 1, "quantity": 5},  # exceeds stock
            {"product_id": pid + 999, "quantity": 1},  # missing product
            {"product_id": pid, "variant_id": 9999, "quantity": 1},  # missing variant
        ]
    }
    r_guest = client.post("/api/v1/catalog/validate-cart", json=payload)
    assert r_guest.status_code == 200
    data_guest = r_guest.json()["items"]
    # Non-variant allowed as requested
    assert data_guest[0]["allowed_quantity"] == 3
    assert data_guest[0]["available"] is True
    # Variant reduced to available stock (2)
    assert data_guest[1]["allowed_quantity"] == 2
    assert data_guest[1]["available"] is True
    assert "reduced" in (data_guest[1]["message"] or "")
    # Missing product is unavailable
    assert data_guest[2]["available"] is False
    # Missing variant is unavailable
    assert data_guest[3]["available"] is False

    # Auth user should receive identical validation results
    r_user = client.post("/api/v1/catalog/validate-cart", json=payload, headers=headers_user())
    assert r_user.status_code == 200
    assert r_user.json() == r_guest.json()


def test_checkout_requires_auth(setup_test_database: None, client: TestClient) -> None:
    # Attempt to add to customer cart without auth -> forbidden
    r_guest = client.post("/api/v1/customer/cart/items", json={"product_id": 1, "quantity": 1})
    assert r_guest.status_code in (401, 403)
    # With auth, allowed (service seeds stub product in tests if missing)
    r_user = client.post(
        "/api/v1/customer/cart/items",
        json={"product_id": 1, "quantity": 1},
        headers=headers_user(),
    )
    assert r_user.status_code == 200