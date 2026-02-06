
"""
wishlist.py

SQLAlchemy ORM model for the wishlist table.
Represents a user's wishlist, including creation and update timestamps.
"""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING, List
import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .wishlist_item import WishlistItem


class Wishlist(Base):
    __tablename__ = 'wishlist'
    wishlist_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.user_id'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    items: Mapped[List['WishlistItem']] = relationship('WishlistItem', back_populates='wishlist', cascade='all, delete-orphan')
