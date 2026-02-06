
# ------------------------------------------------------------------------------
# seller_component.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the seller_component table.
# This module defines the SellerComponent class, which represents a component
# associated with a seller. Each component has an image URL and a description.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import Any
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class SellerComponent(Base):
    """
    ORM model for the 'seller_component' table.
    Represents a component associated with a seller.

    Attributes:
        id (Integer): Primary key for the component.
        img_url (String): URL to an image representing the component.
        description (String): Textual description of the component.
    """
    __tablename__ = 'seller_component'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    img_url: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
