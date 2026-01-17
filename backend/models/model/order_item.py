"""
order_item.py

Expose the canonical OrderItem ORM model from the persistence layer to avoid
duplicate table declarations. Use backend.persistance.order_item.OrderItem as
the single source of truth for the 'order_item' table.
"""

from backend.persistance.order_item import OrderItem  # re-export canonical ORM model

__all__ = ["OrderItem"]
