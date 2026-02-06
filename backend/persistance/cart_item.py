
# ------------------------------------------------------------------------------
# cart_item.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the cart_item table.
# This module defines the CartItem class, which represents an item in a user's
# shopping cart. Each cart item is associated with a cart, a product, and
# optionally a product variant.
# ------------------------------------------------------------------------------


from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from sqlalchemy import BigInteger, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .cart import Cart


class CartItem(Base):
    __tablename__ = 'cart_item'
    cart_item_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cart_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('cart.cart_id'))
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('product.product_id'))
    variant_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey('product_variant.variant_id'), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    cart: Mapped['Cart'] = relationship('Cart', back_populates='items')
