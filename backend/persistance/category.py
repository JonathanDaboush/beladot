# For forward references in type annotations
from __future__ import annotations

# ------------------------------------------------------------------------------
# category.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the category table.
# This module defines the Category class, which represents a product category.
# Each category can have a name and an optional image URL. Relationships to
# subcategories and products are defined elsewhere.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from .subcategory import Subcategory
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base

class Category(Base):
    """
    ORM model for the 'category' table.
    Represents a product category in the catalog.

    Attributes:
        category_id (BigInteger): Primary key for the category.
        name (String): Name of the category.
        image_url (String): URL to an image representing the category (optional).
        # Relationships to subcategories and products are defined elsewhere.
    """
    __tablename__ = 'category'
    category_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    subcategories: Mapped[List['Subcategory']] = relationship(
        "Subcategory",
        back_populates="category",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
