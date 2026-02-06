
# ------------------------------------------------------------------------------
# shipment_address.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the shipment_address table.
# This module defines the ShipmentAddress class, which represents the address
# associated with a shipment. Tracks recipient, address fields, and phone number.
# ------------------------------------------------------------------------------


from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class ShipmentAddress(Base):
    __tablename__ = 'shipment_address'
    shipment_address_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    shipment_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('shipment.shipment_id'))
    recipient_name: Mapped[str] = mapped_column(String(255))
    address_line_1: Mapped[str] = mapped_column(String(255))
    address_line_2: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(100))
    state_province: Mapped[str] = mapped_column(String(100))
    postal_code: Mapped[str] = mapped_column(String(20))
    country: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(String(20))
    # Relationships (to be completed in shipment.py)
