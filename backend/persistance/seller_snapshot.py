
# ------------------------------------------------------------------------------
# seller_snapshot.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the seller_snapshot table.
# This module defines the SellerSnapshot class, which represents a snapshot of a
# seller's details at a specific point in time. Used for historical or auditing purposes.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from backend.db.base import Base

class SellerSnapshot(Base):
    """
    ORM model for the 'seller_snapshot' table.
    Represents a snapshot of a seller's details for historical/auditing purposes.

    Attributes:
        store_name (String): Name of the seller's store (primary key).
        contact_email (String): Contact email for the seller.
        seller_type (String): Type/category of the seller.
        approved_by_name (String): Name of the person who approved the seller.
    """
    __tablename__ = 'seller_snapshot'
    store_name: Mapped[str] = mapped_column(String(255), primary_key=True)
    contact_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    seller_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    approved_by_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
