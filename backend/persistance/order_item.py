"""
order_item.py

SQLAlchemy ORM model for the order_item table.
Represents an item within an order, including product and variant details.
"""

from typing import Optional
from sqlalchemy import BigInteger, Integer, Float, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class OrderItem(Base):
	__tablename__ = 'order_item'
	order_item_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
	order_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('order.order_id'))
	product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('product.product_id'))
	variant_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey('product_variant.variant_id'), nullable=True)
	quantity: Mapped[int] = mapped_column(Integer, nullable=False)
	subtotal: Mapped[float] = mapped_column(Float, nullable=False)
	is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

__all__ = ["OrderItem"]
