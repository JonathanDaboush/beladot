import os
import pytest
from fastapi.testclient import TestClient

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
from fastapi.testclient import TestClient
from backend.app import app


def test_catalog_list_products_public_ok():
    client = TestClient(app)
    res = client.get("/api/v1/catalog/products")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert "items" in data
    assert isinstance(data["items"], list)


def test_catalog_get_product_alias_404_when_missing():
    client = TestClient(app)
    res = client.get("/api/product/999999")
    assert res.status_code == 404
    data = res.json()
    assert "detail" in data


def test_catalog_get_product_public_404_when_missing():
    client = TestClient(app)
    res = client.get("/api/v1/catalog/products/999999")
    assert res.status_code == 404
    data = res.json()
    assert "detail" in data
