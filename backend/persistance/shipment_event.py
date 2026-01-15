
# ------------------------------------------------------------------------------
# shipment_event.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the shipment_event table.
# This module defines the ShipmentEvent class, which represents an event in the
# lifecycle of a shipment. Tracks status, description, location, and timestamp.
# ------------------------------------------------------------------------------

from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class ShipmentEvent(Base):
    """
    ORM model for the 'shipment_event' table.
    Represents an event in the lifecycle of a shipment.

    Attributes:
        event_id (BigInteger): Primary key for the event.
        shipment_id (BigInteger): Foreign key referencing the shipment.
        status (String): Status of the shipment at the time of the event.
        description (Text): Description of the event.
        location (String): Location where the event occurred.
        occurred_at (DateTime): Timestamp when the event occurred.
        # Relationships to shipment are defined elsewhere.
    """
    __tablename__ = 'shipment_event'
    event_id = Column(BigInteger, primary_key=True)
    shipment_id = Column(BigInteger, ForeignKey('shipment.shipment_id'))
    status = Column(String(50))
    description = Column(Text)
    location = Column(String(255))
    occurred_at = Column(DateTime)
    # Relationships (to be completed in shipment.py)
