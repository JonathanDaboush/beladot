
# ------------------------------------------------------------------------------
# employee_snapshot.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the employee_snapshot table.
# This module defines the EmployeeSnapshot class, which represents a snapshot of
# an employee's details at a specific point in time. Used for historical or
# auditing purposes.
# ------------------------------------------------------------------------------

from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

# Base class for all ORM models in the persistence layer.
Base = declarative_base()

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
    full_name = Column(String(255), primary_key=True)
    department_name = Column(String(100))
    role = Column(String(50))
    approved_by_name = Column(String(255))
