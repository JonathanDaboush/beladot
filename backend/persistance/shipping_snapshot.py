"""
shipping_snapshot.py

SQLAlchemy ORM model for the shipping_snapshot table.
Represents a snapshot of a shipment, including events, items, and total cost.
"""


from __future__ import annotations

from typing import List, Dict, Any, Optional
import datetime

from sqlalchemy import BigInteger, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
import json

class ShippingSnapshot(Base):
    __tablename__ = 'shipping_snapshot'
    snapshot_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    shipment_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('shipment.shipment_id'), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)  # 'complete', 'partial', 'failed'
    events: Mapped[str] = mapped_column(Text, nullable=False, default='[]')  # JSON string of event dicts
    items: Mapped[str] = mapped_column(Text, nullable=False, default='[]')   # JSON string of item dicts
    total_cost: Mapped[float] = mapped_column(Float)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    def set_events(self, events_list: List[Dict[str, Any]]) -> None:
        """
        Set the events field as a JSON string from a list.
        Args:
            events_list (list): List of event dicts.
        """
        self.events = json.dumps(events_list)

    def get_events(self) -> List[Dict[str, Any]]:
        """
        Get the events field as a list from JSON string.
        Returns:
            list: List of event dicts.
        """
        return json.loads(self.events) if self.events else []

    def set_items(self, items_list: List[Dict[str, Any]]) -> None:
        """
        Set the items field as a JSON string from a list.
        Args:
            items_list (list): List of item dicts.
        """
        self.items = json.dumps(items_list)

    def get_items(self) -> List[Dict[str, Any]]:
        """
        Get the items field as a list from JSON string.
        Returns:
            list: List of item dicts.
        """
        return json.loads(self.items) if self.items else []

    # Avoid custom __init__ that breaks SQLAlchemy construction; use defaults above.
