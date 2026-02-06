import os
import sys
import pytest

@pytest.fixture(scope="function")
def setup_test_database():
    os.environ["ENV"] = "test"
    from backend.config import settings
    os.environ["DATABASE_URL"] = settings.DATABASE_URL
    from backend.db.base import Base
    from backend.persistance.base import get_engine
    engine = get_engine()
    Base.metadata.drop_all(engine)
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

# Ensure backend is importable when running from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from backend.models.model.refund_request import RefundRequest

def test_refund_request_description():
    from backend.models.model.refund_request import RefundRequestStatus
    refund = RefundRequest(
        refund_request_id=1,
        order_id=10,
        order_item_ids=[100, 101],
        reason="Damaged item",
        status=RefundRequestStatus.PENDING,
        description="Customer reported item was broken on arrival."
    )
    assert refund.description == "Customer reported item was broken on arrival."
    assert refund.reason == "Damaged item"
    assert refund.status == RefundRequestStatus.PENDING
