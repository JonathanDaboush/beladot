
# ------------------------------------------------------------------------------
# order.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the order table.
# This module defines the Order class, which represents a customer order. Tracks
# user, cart, status, total amount, and timestamps. Relationships to order items
# and related models are defined elsewhere.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import Optional
import datetime
from sqlalchemy import BigInteger, Numeric, DateTime, Enum, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from .base import Base
from .enums import OrderStatusEnum

class Order(Base):
    """
    ORM model for the 'order' table.
    Represents a customer order.

    Attributes:
        order_id (BigInteger): Primary key for the order.
        user_id (BigInteger): Foreign key referencing the user who placed the order.
        cart_id (BigInteger): Foreign key referencing the cart (optional).
        order_status (Enum): Status of the order (see OrderStatusEnum).
        total_amount (Numeric): Total amount for the order.
        created_at (DateTime): Timestamp when the order was created.
        updated_at (DateTime): Timestamp when the order was last updated.
        order_number (BigInteger): Unique order number for reference.
        # Relationships to order items and related models are defined elsewhere.
    """
    __tablename__ = 'order'
    order_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.user_id'))
    cart_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey('cart.cart_id'), nullable=True)
    product_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey('product.product_id'), nullable=True)
    order_status: Mapped[OrderStatusEnum] = mapped_column(Enum(OrderStatusEnum))
    total_amount: Mapped[float] = mapped_column(Numeric(10,2))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    order_number: Mapped[int] = mapped_column(BigInteger)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # Relationships (to be completed in related models)
