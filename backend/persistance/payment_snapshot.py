
# ------------------------------------------------------------------------------
# payment_snapshot.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the payment_snapshot table.
# This module defines the PaymentSnapshot class, which represents a snapshot of
# a payment at a specific point in time. Used for historical or auditing purposes.
# ------------------------------------------------------------------------------

from sqlalchemy import Column, String, Numeric, DateTime
from backend.db.base import Base
import datetime

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
    id = Column(String(50), primary_key=True)
    user_full_name = Column(String(255))
    order_number = Column(String(50))
    amount = Column(Numeric(12,2))
    currency = Column(String(10))
    payment_method = Column(String(50))
    last4_digits = Column(String(4))
    status = Column(String(50))
    approved_by_name = Column(String(255))
    date_of_creation = Column(DateTime, default=datetime.datetime.utcnow)
