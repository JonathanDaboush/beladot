"""
Aggregate imports for ORM models so SQLAlchemy's Base.metadata is fully populated
at runtime for migrations, testing, and app startup.

Import modules that declare tables and relationships referenced across the app
and tests. Keep this list in sync with new models as they are added.
"""

# Core
from .user import User  # noqa: F401

# Catalog
from .category import Category  # noqa: F401
from .subcategory import Subcategory  # noqa: F401
from .product import Product  # noqa: F401
from .product_variant import ProductVariant  # noqa: F401

# Images / reviews (optional, extend as needed)
from .product_image import ProductImage  # noqa: F401
from .product_comment import ProductComment  # noqa: F401
from .product_review import ProductReview  # noqa: F401
from .product_rating import ProductRating  # noqa: F401


# Cart / order (optional, extend as needed)
from .cart import Cart  # noqa: F401
from .cart_item import CartItem  # noqa: F401
from .order import Order  # noqa: F401
from .order_item import OrderItem  # noqa: F401

# Wishlist
from .wishlist import Wishlist  # noqa: F401
from .wishlist_item import WishlistItem  # noqa: F401
