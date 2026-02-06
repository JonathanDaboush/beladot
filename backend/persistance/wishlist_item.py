"""
wishlist_item.py

SQLAlchemy ORM model for the wishlist_item table.
Represents an item in a user's wishlist, including product, variant, and quantity.
"""


from typing import Optional, TYPE_CHECKING
from sqlalchemy import BigInteger, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .wishlist import Wishlist

class WishlistItem(Base):
    __tablename__ = 'wishlist_item'
    wishlist_item_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    wishlist_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('wishlist.wishlist_id'))
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('product.product_id'))
    variant_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey('product_variant.variant_id'), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.user_id'))  # Updated ForeignKey reference
    user: Mapped['User'] = relationship('User', back_populates='wishlist_items')
    wishlist: Mapped['Wishlist'] = relationship('Wishlist', back_populates='items')
