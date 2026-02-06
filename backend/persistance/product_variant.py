
# ------------------------------------------------------------------------------
# product_variant.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the product_variant table.
# This module defines the ProductVariant class, which represents a variant of a
# product (e.g., size, color). Tracks variant name, price, quantity, and status.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import Optional
from sqlalchemy import BigInteger, String, Numeric, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class ProductVariant(Base):
    """
    ORM model for the 'product_variant' table.
    Represents a variant of a product (e.g., size, color).

    Attributes:
        variant_id (BigInteger): Primary key for the variant.
        product_id (BigInteger): Foreign key referencing the product.
        variant_name (String): Name of the variant (e.g., 'Large', 'Red').
        price (Numeric): Price for this variant.
        quantity (Integer): Number of units available for this variant.
        is_active (Boolean): Whether the variant is currently active/listed.
        # Relationships to related models are defined elsewhere.
    """
    __tablename__ = 'product_variant'
    variant_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('product.product_id'))
    variant_name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Numeric(10,2))
    quantity: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    # Relationships (to be completed in related models)
