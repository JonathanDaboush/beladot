"""
ledger.py

SQLAlchemy ORM model for ledger entries.
Represents a financial transaction or event in the system ledger.
"""


from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float, DateTime
from datetime import datetime
from backend.db.base import Base

class LedgerEntry(Base):
    __tablename__ = "ledger"

    ledger_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    entry_type: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    # `DomainEvent` is defined as a dataclass (not persisted to its own table).
    # Keep `event_ref` as a nullable integer reference without a DB-level ForeignKey
    # to avoid metadata resolution errors during test database creation.
    event_ref: Mapped[int] = mapped_column(Integer, nullable=True)
    actor: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
