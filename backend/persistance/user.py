"""
user.py

SQLAlchemy ORM model for the user table.
Represents a user, including personal and account information.
"""

from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .wishlist_item import WishlistItem


class User(Base):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    dob: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    created_at: Mapped[Optional[Date]] = mapped_column(Date, nullable=True)
    img_location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    account_status: Mapped[str] = mapped_column(String(5), nullable=False, default='True')
    # Relationships (to be completed in other models)
    wishlist_items: Mapped[List['WishlistItem']] = relationship(
        "WishlistItem",
        back_populates="user",
        cascade="all, delete-orphan"
    )
