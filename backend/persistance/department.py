
# ------------------------------------------------------------------------------
# department.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the department table.
# This module defines the Department class, which represents a department within
# the organization. Each department has a unique ID and a name. Relationships to
# managers, shifts, and employees are defined elsewhere.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .manager import Manager

class Department(Base):
    """
    ORM model for the 'department' table.
    Represents a department within the organization.

    Attributes:
        department_id (BigInteger): Primary key for the department.
        name (String): Name of the department.
        # Relationships to managers, shifts, and employees are defined elsewhere.
    """
    __tablename__ = 'department'
    department_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    # Relationships (to be completed in manager.py, shift.py, employee.py)
