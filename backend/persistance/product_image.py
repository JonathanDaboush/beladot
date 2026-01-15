
# ------------------------------------------------------------------------------
# product_image.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the product_image table.
# This module defines the ProductImage class, which represents an image
# associated with a product. Each image is linked to a product.
# ------------------------------------------------------------------------------

from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class ProductImage(Base):
    """
    ORM model for the 'product_image' table.
    Represents an image associated with a product.

    Attributes:
        image_id (BigInteger): Primary key for the image.
        product_id (BigInteger): Foreign key referencing the product.
        image_url (String): URL to the image file.
        # Relationship to product is defined elsewhere.
    """
    __tablename__ = 'product_image'
    image_id = Column(BigInteger, primary_key=True)
    product_id = Column(BigInteger, ForeignKey('product.product_id'))
    image_url = Column(String(255))
    # Relationship (to be completed in product.py)
