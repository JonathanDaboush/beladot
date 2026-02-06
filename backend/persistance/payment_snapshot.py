
# ------------------------------------------------------------------------------
# payment_snapshot.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the payment_snapshot table.
# This module defines the PaymentSnapshot class, which represents a snapshot of
# a payment at a specific point in time. Used for historical or auditing purposes.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import Optional
import datetime
from sqlalchemy import String, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from backend.db.base import Base

# Base provided by backend.db.base

class PaymentSnapshot(Base):
    """
    ORM model for the 'payment_snapshot' table.
    Represents a snapshot of a payment for historical/auditing purposes.

    Attributes:
        user_full_name (String): Full name of the user who made the payment.
        order_number (String): Order number associated with the payment.
        amount (Numeric): Amount paid.
        currency (String): Currency of the payment.
        payment_method (String): Payment method used (e.g., credit card, PayPal).
        last4_digits (String): Last 4 digits of the payment card (if applicable).
        status (String): Status of the payment at the time of the snapshot.
        approved_by_name (String): Name of the person who approved the payment.
        date_of_creation (DateTime): Timestamp when the snapshot was created.
    """
    __tablename__ = 'payment_snapshot'
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    user_full_name: Mapped[str] = mapped_column(String(255))
    order_number: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float] = mapped_column(Numeric(12,2))
    currency: Mapped[str] = mapped_column(String(10))
    payment_method: Mapped[str] = mapped_column(String(50))
    last4_digits: Mapped[str] = mapped_column(String(4))
    status: Mapped[str] = mapped_column(String(50))
    approved_by_name: Mapped[str] = mapped_column(String(255))
    date_of_creation: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, default=datetime.datetime.utcnow)
