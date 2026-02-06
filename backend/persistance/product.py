
# ------------------------------------------------------------------------------
# product.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the product table.
# This module defines the Product class, which represents a product listed by a
# seller. Tracks category, subcategory, pricing, status, and timestamps.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import Optional
import datetime
from sqlalchemy import Integer, BigInteger, String, Text, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Product(Base):
    """
    ORM model for the 'product' table.
    Represents a product listed by a seller.

    Attributes:
        product_id (BigInteger): Primary key for the product.
        seller_id (BigInteger): Foreign key referencing the seller (user).
        category_id (BigInteger): Foreign key referencing the product category.
        subcategory_id (BigInteger): Foreign key referencing the product subcategory.
        title (String): Title of the product.
        description (Text): Description of the product.
        price (Numeric): Price of the product.
        currency (String): Currency of the price.
        is_active (Boolean): Whether the product is currently active/listed.
        created_at (DateTime): Timestamp when the product was created.
        updated_at (DateTime): Timestamp when the product was last updated.
        # Relationships to related models are defined elsewhere.
    """
    __tablename__ = 'product'
    # Use Integer for SQLite autoincrement primary key behavior
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    seller_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.user_id'))
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('category.category_id'))
    subcategory_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey('subcategory.subcategory_id'), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10,2))
    currency: Mapped[str] = mapped_column(String(10))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # Relationships (to be completed in related models)
    
    @property
    def name(self) -> str:
        """Compatibility alias used by services expecting `name`."""
        return self.title
    
    @name.setter
    def name(self, value: str) -> None:
        """Allow setting name by updating title."""
        self.title = value

    # Provide a lightweight `stock` attribute for code that reads/writes it
    # without changing the DB schema here. This uses a private attribute so
    # it won't be persisted unless elsewhere mapped.
    @property
    def stock(self) -> int:
        return getattr(self, '_stock', 0)

    @stock.setter
    def stock(self, value: int) -> None:
        setattr(self, '_stock', value)
