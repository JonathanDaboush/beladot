
# ------------------------------------------------------------------------------
# cart.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the cart table.
# This module defines the Cart class, which represents a user's shopping cart.
# Each cart is associated with a user and contains metadata about creation and
# update times. Relationships to cart items are defined in cart_item.py.
# ------------------------------------------------------------------------------


from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING
import datetime

from sqlalchemy import Integer, BigInteger, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .cart_item import CartItem


class Cart(Base):
    __tablename__ = 'cart'
    cart_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.user_id'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    items: Mapped[List['CartItem']] = relationship('CartItem', back_populates='cart', cascade='all, delete-orphan')
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
