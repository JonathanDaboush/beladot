
# ------------------------------------------------------------------------------
# return_shipment.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the return_shipment table.
# This module defines the ReturnShipment class, which represents a return
# shipment for an order. Tracks original shipment, status, and timestamps.
# ------------------------------------------------------------------------------

from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class ReturnShipment(Base):
    """
    ORM model for the 'return_shipment' table.
    Represents a return shipment for an order.

    Attributes:
        return_shipment_id (BigInteger): Primary key for the return shipment.
        original_shipment_id (BigInteger): Foreign key referencing the original shipment.
        return_status (String): Status of the return shipment.
        shipped_at (DateTime): Timestamp when the return shipment was shipped.
        received_at (DateTime): Timestamp when the return shipment was received.
        # Relationships to shipment are defined elsewhere.
    """
    __tablename__ = 'return_shipment'
    return_shipment_id = Column(BigInteger, primary_key=True)
    original_shipment_id = Column(BigInteger, ForeignKey('shipment.shipment_id'))
    return_status = Column(String(50))
    shipped_at = Column(DateTime)
    received_at = Column(DateTime)
    # Relationships (to be completed in shipment.py)
