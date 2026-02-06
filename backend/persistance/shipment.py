"""
shipment.py

SQLAlchemy ORM model for the shipment table.
Represents a shipment for an order, including status and timestamps.
"""


from __future__ import annotations

from typing import Optional
import datetime
from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .enums import ShipmentStatusEnum

class Shipment(Base):
    __tablename__ = 'shipment'
    shipment_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('order.order_id'))
    shipment_status: Mapped[ShipmentStatusEnum] = mapped_column(Enum(ShipmentStatusEnum))
    shipped_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    delivered_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    # Relationships (to be completed in related models)
