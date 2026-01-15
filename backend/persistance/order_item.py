
# ------------------------------------------------------------------------------
# order_item.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the order_item table.
# This module defines the OrderItem class, which represents an item within a
# customer order. Tracks product, variant, quantity, and subtotal for each item.
# ------------------------------------------------------------------------------

from sqlalchemy import Column, BigInteger, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class OrderItem(Base):
    """
    ORM model for the 'order_item' table.
    Represents an item within a customer order.

    Attributes:
        order_item_id (BigInteger): Primary key for the order item.
        order_id (BigInteger): Foreign key referencing the order.
        product_id (BigInteger): Foreign key referencing the product.
        variant_id (BigInteger): Foreign key referencing the product variant (optional).
        quantity (Integer): Number of units of the product in the order.
        subtotal (Numeric): Subtotal amount for this order item.
        # Relationships to order, product, and product_variant are defined elsewhere.
    """
    __tablename__ = 'order_item'
    order_item_id = Column(BigInteger, primary_key=True)
    order_id = Column(BigInteger, ForeignKey('order.order_id'))
    product_id = Column(BigInteger, ForeignKey('product.product_id'))
    variant_id = Column(BigInteger, ForeignKey('product_variant.variant_id'), nullable=True)
    quantity = Column(Integer)
    subtotal = Column(Numeric(10,2))
    # Relationships (to be completed in order.py, product.py, product_variant.py)
