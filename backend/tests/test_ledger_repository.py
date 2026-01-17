import os
import sys
import asyncio
import pytest

# Ensure backend is importable when running from project root
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
)


class FakeAsyncSession:
    def __init__(self):
        self.add_called_with = []
        self.commit_called = 0
        self.refresh_called_with = []

    def add(self, obj):
        self.add_called_with.append(obj)

    async def commit(self):
        self.commit_called += 1

    async def refresh(self, obj):
        self.refresh_called_with.append(obj)


def test_ledger_repository_save_calls_session_methods():
    from backend.repositories.repository.ledger_repository import LedgerRepository
    from backend.models.model.ledger import LedgerEntry
    from backend.models.model.domain_event import DomainEvent, DomainEventType

    async def run():
        fake_session = FakeAsyncSession()
        repo = LedgerRepository(fake_session)
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
