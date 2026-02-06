
# ------------------------------------------------------------------------------
# employee_snapshot.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the employee_snapshot table.
# This module defines the EmployeeSnapshot class, which represents a snapshot of
# an employee's details at a specific point in time. Used for historical or
# auditing purposes.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from backend.db.base import Base

class EmployeeSnapshot(Base):
    """
    ORM model for the 'employee_snapshot' table.
    Represents a snapshot of an employee's details for historical/auditing purposes.

    Attributes:
        full_name (String): Full name of the employee (primary key).
        department_name (String): Name of the department at the time of the snapshot.
        role (String): Role or position of the employee.
        approved_by_name (String): Name of the person who approved the snapshot.
    """
    __tablename__ = 'employee_snapshot'
    full_name: Mapped[str] = mapped_column(String(255), primary_key=True)
    department_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    role: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    approved_by_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
