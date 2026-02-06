"""
refund_ledger.py

SQLAlchemy ORM model for refund ledger entries.
Represents a ledger entry for refund actions and amounts.
"""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float, DateTime
from datetime import datetime
from backend.db.base import Base

class RefundLedger(Base):
    __tablename__ = "refund_ledger"

    refund_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    action: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
