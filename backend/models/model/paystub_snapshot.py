"""
paystub_snapshot.py

Expose the canonical PaystubSnapshot ORM model from the persistence layer to
avoid duplicate table declarations.
"""

from backend.persistance.paystub_snapshot import PaystubSnapshot

__all__ = ["PaystubSnapshot"]
