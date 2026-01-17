"""
payment_snapshot.py

Expose the canonical PaymentSnapshot ORM model from the persistence layer to
avoid duplicate table declarations.
"""

from backend.persistance.payment_snapshot import PaymentSnapshot

__all__ = ["PaymentSnapshot"]
