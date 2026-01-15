
# ------------------------------------------------------------------------------
# cart.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the cart table.
# This module defines the Cart class, which represents a user's shopping cart.
# Each cart is associated with a user and contains metadata about creation and
# update times. Relationships to cart items are defined in cart_item.py.
# ------------------------------------------------------------------------------

from sqlalchemy import Column, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Cart(Base):
    """
    ORM model for the 'cart' table.
    Represents a user's shopping cart, which can contain multiple items.

    Attributes:
        cart_id (BigInteger): Primary key for the cart.
        user_id (BigInteger): Foreign key referencing the user who owns the cart.
        created_at (DateTime): Timestamp when the cart was created.
        updated_at (DateTime): Timestamp when the cart was last updated.
        # Relationships to cart items are defined in cart_item.py.
    """
    __tablename__ = 'cart'
    cart_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('user.user_id'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    # Relationships (to be completed in cart_item.py)
