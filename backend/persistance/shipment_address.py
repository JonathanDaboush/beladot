
# ------------------------------------------------------------------------------
# shipment_address.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the shipment_address table.
# This module defines the ShipmentAddress class, which represents the address
# associated with a shipment. Tracks recipient, address fields, and phone number.
# ------------------------------------------------------------------------------

from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class ShipmentAddress(Base):
    """
    ORM model for the 'shipment_address' table.
    Represents the address associated with a shipment.

    Attributes:
        shipment_address_id (BigInteger): Primary key for the shipment address.
        shipment_id (BigInteger): Foreign key referencing the shipment.
        recipient_name (String): Name of the recipient.
        address_line_1 (String): First line of the address.
        address_line_2 (String): Second line of the address (optional).
        city (String): City of the address.
        state_province (String): State or province of the address.
        postal_code (String): Postal or ZIP code.
        country (String): Country of the address.
        phone_number (String): Contact phone number for the recipient.
        # Relationships to shipment are defined elsewhere.
    """
    __tablename__ = 'shipment_address'
    shipment_address_id = Column(BigInteger, primary_key=True)
    shipment_id = Column(BigInteger, ForeignKey('shipment.shipment_id'))
    recipient_name = Column(String(255))
    address_line_1 = Column(String(255))
    address_line_2 = Column(String(255))
    city = Column(String(100))
    state_province = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(100))
    phone_number = Column(String(20))
    # Relationships (to be completed in shipment.py)
