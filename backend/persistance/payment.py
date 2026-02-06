
# ------------------------------------------------------------------------------
# payment.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the payment table.
# This module defines the Payment class, which represents a payment made for an
# order. Tracks user, order, amount, currency, status, and timestamps.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import Optional
import datetime
from sqlalchemy import BigInteger, Numeric, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from .base import Base
from .enums import PaymentStatusEnum

class Payment(Base):
    """
    ORM model for the 'payment' table.
    Represents a payment made for an order.

    Attributes:
        payment_id (BigInteger): Primary key for the payment.
        order_id (BigInteger): Foreign key referencing the order.
        user_id (BigInteger): Foreign key referencing the user who made the payment.
        amount (Numeric): Amount paid.
        currency (String): Currency of the payment.
        status (Enum): Status of the payment (see PaymentStatusEnum).
        created_at (DateTime): Timestamp when the payment was created.
        updated_at (DateTime): Timestamp when the payment was last updated.
        # Relationships to order are defined elsewhere.
    """
    __tablename__ = 'payment'
    payment_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    order_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('order.order_id'))
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.user_id'))
    amount: Mapped[float] = mapped_column(Numeric(10,2))
    currency: Mapped[str] = mapped_column(String(10))
    status: Mapped['PaymentStatusEnum'] = mapped_column(Enum(PaymentStatusEnum))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    # Relationships (to be completed in order.py)
