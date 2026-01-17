"""
employee_snapshot.py

Expose the canonical EmployeeSnapshot ORM model from the persistence layer to
avoid duplicate table declarations.
"""

from backend.persistance.employee_snapshot import EmployeeSnapshot

__all__ = ["EmployeeSnapshot"]
