"""
pto_snapshot.py

Expose the canonical PTOSnapshot ORM model from the persistence layer to
avoid duplicate table declarations.
"""

from backend.persistance.pto_snapshot import PTOSnapshot

__all__ = ["PTOSnapshot"]
