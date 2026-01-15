
# ------------------------------------------------------------------------------
# product_variant_image.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the product_variant_image table.
# This module defines the ProductVariantImage class, which represents an image
# associated with a product variant. Each image is linked to a variant.
# ------------------------------------------------------------------------------

from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship
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
    image_id = Column(BigInteger, primary_key=True)
    variant_id = Column(BigInteger, ForeignKey('product_variant.variant_id'))
    image_url = Column(String(255))
    # Relationship (to be completed in product_variant.py)
