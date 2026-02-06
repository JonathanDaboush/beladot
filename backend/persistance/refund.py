
# ------------------------------------------------------------------------------
# refund.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the refund table.
# This module defines the Refund class, which represents a refund transaction.
# Tracks payment, order item, amount, reason, approval, status, and timestamps.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import Optional
import datetime
from sqlalchemy import BigInteger, Numeric, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from .base import Base
from .enums import RefundStatusEnum
from . import payment  # ensure payment table is registered in metadata

class Refund(Base):
    """
    ORM model for the 'refund' table.
    Represents a refund transaction.

    Attributes:
        refund_id (BigInteger): Primary key for the refund.
        payment_id (BigInteger): Foreign key referencing the payment.
        order_item_id (BigInteger): Foreign key referencing the order item (optional).
        amount (Numeric): Amount refunded.
        reason (Text): Reason for the refund.
        approved_by_cs_id (BigInteger): Foreign key referencing the approving customer service employee (optional).
        status (Enum): Status of the refund (see RefundStatusEnum).
        created_at (DateTime): Timestamp when the refund was created.
        processed_at (DateTime): Timestamp when the refund was processed.
        # Relationships to payment, order_item, and employee are defined elsewhere.
    """
    __tablename__ = 'refund'
    refund_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    payment_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('payment.payment_id'))
    order_item_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey('order_item.order_item_id'), nullable=True)
    amount: Mapped[float] = mapped_column(Numeric(10,2))
    reason: Mapped[str] = mapped_column(Text)
    approved_by_cs_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey('employee.emp_id'), nullable=True)
    status: Mapped[RefundStatusEnum] = mapped_column(Enum(RefundStatusEnum))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    processed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    # Relationships (to be completed in payment.py, order_item.py, employee.py)
