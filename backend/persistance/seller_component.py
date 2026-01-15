
# ------------------------------------------------------------------------------
# seller_component.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the seller_component table.
# This module defines the SellerComponent class, which represents a component
# associated with a seller. Each component has an image URL and a description.
# ------------------------------------------------------------------------------

from sqlalchemy import Column, Integer, String
from backend.persistance.base import Base

class SellerComponent(Base):
    """
    ORM model for the 'seller_component' table.
    Represents a component associated with a seller.

    Attributes:
        id (Integer): Primary key for the component.
        img_url (String): URL to an image representing the component.
        description (String): Textual description of the component.
    """
    __tablename__ = 'seller_component'
    id = Column(Integer, primary_key=True, autoincrement=True)
    img_url = Column(String, nullable=False)
    description = Column(String, nullable=False)
