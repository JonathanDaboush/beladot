"""
order_item.py

SQLAlchemy ORM model for the order_item table.
Represents an item within an order, including product and variant details.
"""

from sqlalchemy import Column, BigInteger, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class OrderItem(Base):
	__tablename__ = 'order_item'
	order_item_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
	order_id = Column(BigInteger, ForeignKey('order.order_id'))
	product_id = Column(BigInteger, ForeignKey('product.product_id'))
	variant_id = Column(BigInteger, ForeignKey('product_variant.variant_id'), nullable=True)
	quantity = Column(Integer, nullable=False)
	subtotal = Column(Float, nullable=False)

__all__ = ["OrderItem"]
