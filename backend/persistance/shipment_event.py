
# ------------------------------------------------------------------------------
# shipment_event.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the shipment_event table.
# This module defines the ShipmentEvent class, which represents an event in the
# lifecycle of a shipment. Tracks status, description, location, and timestamp.
# ------------------------------------------------------------------------------


from __future__ import annotations

from typing import Optional
import datetime
from sqlalchemy import BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class ShipmentEvent(Base):
    __tablename__ = 'shipment_event'
    event_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    shipment_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('shipment.shipment_id'))
    status: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)
    location: Mapped[str] = mapped_column(String(255))
    occurred_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    # Relationships (to be completed in shipment.py)
