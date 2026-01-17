
# ------------------------------------------------------------------------------
# cart_item.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the cart_item table.
# This module defines the CartItem class, which represents an item in a user's
# shopping cart. Each cart item is associated with a cart, a product, and
# optionally a product variant.
# ------------------------------------------------------------------------------

from sqlalchemy import Column, BigInteger, Integer, ForeignKey
from .base import Base

class CartItem(Base):
    """
    ORM model for the 'cart_item' table.
    Represents an item in a user's shopping cart.

    Attributes:
        cart_item_id (BigInteger): Primary key for the cart item.
        cart_id (BigInteger): Foreign key referencing the cart.
        product_id (BigInteger): Foreign key referencing the product.
        variant_id (BigInteger): Foreign key referencing the product variant (optional).
        quantity (Integer): Number of units of the product in the cart.
        # Relationships to cart, product, and product_variant are defined elsewhere.
    """
    __tablename__ = 'cart_item'
    cart_item_id = Column(BigInteger, primary_key=True)
    cart_id = Column(BigInteger, ForeignKey('cart.cart_id'))
    product_id = Column(BigInteger, ForeignKey('product.product_id'))
    variant_id = Column(BigInteger, ForeignKey('product_variant.variant_id'), nullable=True)
    quantity = Column(Integer)
    # Relationships (to be completed in cart.py, product.py, product_variant.py)
