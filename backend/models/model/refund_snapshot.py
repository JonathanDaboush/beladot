"""
refund_snapshot.py

Expose the canonical RefundSnapshot ORM model from the persistence layer to
avoid duplicate table declarations.
"""

from backend.persistance.refund_snapshot import RefundSnapshot

__all__ = ["RefundSnapshot"]
