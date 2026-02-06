
"""
refund_request.py

SQLAlchemy ORM model for refund requests.
Represents a customer's request for a refund, including the items involved,
reason, status, and optional description. Stores `order_item_ids` as a JSON
string to avoid join proliferation in test environment.
"""

from __future__ import annotations

from typing import Any, List, Optional
import datetime
from sqlalchemy import BigInteger, Text, DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy.orm import validates
from .base import Base


class RefundRequest(Base):
    __tablename__ = 'refund_request'
    refund_request_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('order.order_id'), nullable=False)
    # JSON array of order item ids
    order_item_ids: Mapped[str] = mapped_column(Text, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    date_of_request: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    @validates('order_item_ids')
    def _validate_order_item_ids(self, key: str, value: Any) -> str:
        import json
        if isinstance(value, (list, tuple)):
            return json.dumps(list(value))
        if isinstance(value, str):
            return value
        raise ValueError('order_item_ids must be a list or JSON string')

    def get_order_item_ids(self) -> List[Any]:
        import json
        try:
            return json.loads(self.order_item_ids) if self.order_item_ids else []
        except (ValueError, json.JSONDecodeError) as e:
            try:
                from backend.infrastructure.structured_logging import logger
                logger.error("refund_request.json_decode_failed", error=str(e), order_item_ids=self.order_item_ids)
            except Exception:
                pass
            return []
