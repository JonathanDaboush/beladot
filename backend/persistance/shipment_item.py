"""
shipment_item.py

SQLAlchemy ORM model for the shipment_item table.
Represents an item within a shipment, including product, variant, and status.
"""


from typing import Optional
from sqlalchemy import BigInteger, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class ShipmentItem(Base):
    __tablename__ = 'shipment_item'
    shipment_item_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    shipment_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('shipment.shipment_id'))
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('product.product_id'))
    variant_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey('product_variant.variant_id'), nullable=True)
    shipment_event_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey('shipment_event.event_id'), nullable=True)  # FK to shipment_event
    quantity: Mapped[int] = mapped_column(Integer)
    status: Mapped[int] = mapped_column(Integer, default=0)  # 0: pending, 1: shipped, 2: delivered
    # Relationships (to be completed in shipment.py, product.py, product_variant.py)
