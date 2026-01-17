"""
address_snapshot.py

Expose the canonical AddressSnapshot ORM model from the persistence layer to
avoid duplicate table declarations.
"""

from backend.persistance.address_snapshot import AddressSnapshot

__all__ = ["AddressSnapshot"]
