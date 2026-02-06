
# ------------------------------------------------------------------------------
# address_snapshot.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the address_snapshot table.
# This module defines the AddressSnapshot class, which represents a snapshot of
# an address at a specific point in time. Used for historical or reference
# purposes, such as storing the address associated with an order or shipment.
# ------------------------------------------------------------------------------


from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from backend.db.base import Base

class AddressSnapshot(Base):
    __tablename__ = 'address_snapshot'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    reference_type: Mapped[str] = mapped_column(String(50))
    recipient_name: Mapped[str] = mapped_column(String(255))
    street_line_1: Mapped[str] = mapped_column(String(255))
    street_line_2: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(100))
    state_province: Mapped[str] = mapped_column(String(50))
    postal_code: Mapped[str] = mapped_column(String(20))
    country: Mapped[str] = mapped_column(String(50))
    phone_number: Mapped[str] = mapped_column(String(20))
    order_number: Mapped[str] = mapped_column(String(50))  # Order reference (if applicable)
    shipment_id: Mapped[str] = mapped_column(String(50))   # Shipment reference (if applicable)
