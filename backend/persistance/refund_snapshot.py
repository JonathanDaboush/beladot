
# ------------------------------------------------------------------------------
# refund_snapshot.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the refund_snapshot table.
# This module defines the RefundSnapshot class, which represents a snapshot of a
# refund at a specific point in time. Used for historical or auditing purposes.
# ------------------------------------------------------------------------------

from sqlalchemy import String, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column
from backend.db.base import Base

# Base provided by backend.db.base

class RefundSnapshot(Base):
    """
    ORM model for the 'refund_snapshot' table.
    Represents a snapshot of a refund for historical/auditing purposes.

    Attributes:
        payment_user_name (String): Name of the user who received the refund.
        order_number (String): Order number associated with the refund.
        amount (Numeric): Amount refunded.
        reason (Text): Reason for the refund.
        approved_by_name (String): Name of the person who approved the refund.
        status (String): Status of the refund at the time of the snapshot.
    """
    __tablename__ = 'refund_snapshot'
    id: Mapped[str] = mapped_column(String(50), primary_key=True)  # Add a primary key column
    payment_user_name: Mapped[str] = mapped_column(String(255))
    order_number: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float] = mapped_column(Numeric(12,2))
    reason: Mapped[str] = mapped_column(Text)
    approved_by_name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50))
