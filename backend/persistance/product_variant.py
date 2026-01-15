
# ------------------------------------------------------------------------------
# product_variant.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the product_variant table.
# This module defines the ProductVariant class, which represents a variant of a
# product (e.g., size, color). Tracks variant name, price, quantity, and status.
# ------------------------------------------------------------------------------

from sqlalchemy import Column, BigInteger, String, Numeric, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
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
    variant_id = Column(BigInteger, primary_key=True)
    product_id = Column(BigInteger, ForeignKey('product.product_id'))
    variant_name = Column(String(100))
    price = Column(Numeric(10,2))
    quantity = Column(Integer)
    is_active = Column(Boolean, default=True)
    # Relationships (to be completed in related models)
