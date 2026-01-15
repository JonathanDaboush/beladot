
# ------------------------------------------------------------------------------
# seller_snapshot.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the seller_snapshot table.
# This module defines the SellerSnapshot class, which represents a snapshot of a
# seller's details at a specific point in time. Used for historical or auditing purposes.
# ------------------------------------------------------------------------------

from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

# Base class for all ORM models in the persistence layer.
Base = declarative_base()

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
    store_name = Column(String(255), primary_key=True)
    contact_email = Column(String(255))
    seller_type = Column(String(50))
    approved_by_name = Column(String(255))
