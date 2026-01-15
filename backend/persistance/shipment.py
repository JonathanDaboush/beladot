"""
shipment.py

SQLAlchemy ORM model for the shipment table.
Represents a shipment for an order, including status and timestamps.
"""

from sqlalchemy import Column, BigInteger, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .base import Base
from .enums import ShipmentStatusEnum

class Shipment(Base):
    """
    ORM model for the 'shipment' table.
    Represents a shipment for an order.

    Attributes:
        shipment_id (BigInteger): Primary key for the shipment.
        order_id (BigInteger): Foreign key referencing the order.
        shipment_status (Enum): Status of the shipment (see ShipmentStatusEnum).
        shipped_at (DateTime): Timestamp when the shipment was shipped.
        delivered_at (DateTime): Timestamp when the shipment was delivered.
        created_at (DateTime): Timestamp when the shipment record was created.
        updated_at (DateTime): Timestamp when the shipment record was last updated.
        # Relationships to shipment events and related models are defined elsewhere.
    """
    __tablename__ = 'shipment'
    shipment_id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )
    order_id = Column(BigInteger, ForeignKey('order.order_id'))
    shipment_status = Column(Enum(ShipmentStatusEnum))
    shipped_at = Column(DateTime)
    delivered_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    # Relationships (to be completed in related models)
