from typing import Any
import os
import sys
import asyncio
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

# Ensure backend is importable when running from project root
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)

class FakeAsyncSession:
    def __init__(self):
        self.add_called_with: list[Any] = []
        self.commit_called = 0
        self.refresh_called_with: list[Any] = []

    def add(self, obj: Any) -> None:
        self.add_called_with.append(obj)

    async def commit(self):
        self.commit_called += 1

    async def refresh(self, obj: Any) -> None:
        self.refresh_called_with.append(obj)

def test_ledger_repository_save_calls_session_methods():
    from backend.repositories.repository.ledger_repository import LedgerRepository
    from backend.persistance.ledger import LedgerEntry
    from backend.models.model.domain_event import DomainEvent, DomainEventType

    async def run():
        fake_session = FakeAsyncSession()
        repo = LedgerRepository(fake_session)  # type: ignore
        entry = LedgerEntry(
            entry_type="credit",
            amount=10.0,
            event_ref=DomainEvent(
                event_type=DomainEventType.REFUND_APPROVED,
                entity_id=42,
                actor="tester",
                payload={},
            ),
            actor="tester",
        )
        saved = await repo.save(entry)
        assert saved is entry
        assert fake_session.add_called_with == [entry]
        assert fake_session.commit_called == 1
        assert fake_session.refresh_called_with == [entry]

    asyncio.run(run())
