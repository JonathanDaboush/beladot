"""
shipment.py

Expose the canonical Shipment ORM model from the persistence layer to avoid
duplicate table declarations. Use backend.persistance.shipment.Shipment as the
single source of truth for the 'shipment' table.
"""

from backend.persistance.shipment import Shipment  # re-export canonical ORM model

__all__ = ["Shipment"]


