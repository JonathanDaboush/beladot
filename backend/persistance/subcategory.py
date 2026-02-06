"""
subcategory.py

SQLAlchemy ORM model for the subcategory table.
Represents a subcategory within a category, including name and image URL.
"""


from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .category import Category

class Subcategory(Base):
    __tablename__ = 'subcategory'
    subcategory_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('category.category_id'))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    category: Mapped['Category'] = relationship(
        "Category",
        back_populates="subcategories",
        lazy="selectin"
    )
