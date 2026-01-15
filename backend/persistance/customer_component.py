
# ------------------------------------------------------------------------------
# customer_component.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the seller_component table.
# This module defines the SellerComponent class, which represents a component
# associated with a seller in the database. Each component has an image URL and
# a description. This file is part of the persistence layer and is used by the
# repository and service layers for CRUD operations.
# ------------------------------------------------------------------------------

from sqlalchemy import Column, BigInteger, String
from sqlalchemy.ext.declarative import declarative_base

# Base class for all ORM models in the persistence layer.
Base = declarative_base()

class SellerComponent(Base):
    """
    ORM model for the 'seller_component' table.
    Represents a component (e.g., a product part or feature) associated with a seller.

    Attributes:
        id (BigInteger): Primary key for the component.
        img_url (String): URL to an image representing the component.
        description (String): Textual description of the component.
    """
    __tablename__ = 'seller_component'
    id = Column(BigInteger, primary_key=True)
    img_url = Column(String(255))
    description = Column(String(255))
