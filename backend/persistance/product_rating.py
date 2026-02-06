
# ------------------------------------------------------------------------------
# product_rating.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the product_rating table.
# This module defines the ProductRating class, which represents a rating given
# by a user to a product. Tracks rating value and creation timestamp.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import Optional
import datetime
from sqlalchemy import BigInteger, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class ProductRating(Base):
    """
    ORM model for the 'product_rating' table.
    Represents a rating given by a user to a product.

    Attributes:
        rating_id (BigInteger): Primary key for the rating.
        product_id (BigInteger): Foreign key referencing the product.
        user_id (BigInteger): Foreign key referencing the user who gave the rating.
        rating (Integer): Rating value (e.g., 1-5 stars).
        created_at (DateTime): Timestamp when the rating was created.
        # Relationships to related models are defined elsewhere.
    """
    __tablename__ = 'product_rating'
    rating_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('product.product_id'))
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.user_id'))
    rating: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    # Relationships (to be completed in related models)
