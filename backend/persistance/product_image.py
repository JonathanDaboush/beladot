
# ------------------------------------------------------------------------------
# product_image.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the product_image table.
# This module defines the ProductImage class, which represents an image
# associated with a product. Each image is linked to a product.
# ------------------------------------------------------------------------------


from __future__ import annotations

from typing import Optional
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class ProductImage(Base):
    __tablename__ = 'product_image'
    image_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('product.product_id'))
    image_url: Mapped[str] = mapped_column(String(255))
    # Relationship (to be completed in product.py)
