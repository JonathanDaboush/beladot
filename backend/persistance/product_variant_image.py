
# ------------------------------------------------------------------------------
# product_variant_image.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the product_variant_image table.
# This module defines the ProductVariantImage class, which represents an image
# associated with a product variant. Each image is linked to a variant.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import Optional
from sqlalchemy import BigInteger, String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class ProductVariantImage(Base):
    """
    ORM model for the 'product_variant_image' table.
    Represents an image associated with a product variant.

    Attributes:
        image_id (BigInteger): Primary key for the image.
        variant_id (BigInteger): Foreign key referencing the product variant.
        image_url (String): URL to the image file.
        # Relationship to product_variant is defined elsewhere.
    """
    __tablename__ = 'product_variant_image'
    image_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    variant_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('product_variant.variant_id'))
    image_url: Mapped[str] = mapped_column(String(255))
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # Relationship (to be completed in product_variant.py)
