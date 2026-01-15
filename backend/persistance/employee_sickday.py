
# ------------------------------------------------------------------------------
# employee_sickday.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the employee_sickday table.
# This module defines the EmployeeSickDay class, which represents a sick day
# request by an employee. Includes sick day date, status, and approval info.
# ------------------------------------------------------------------------------

from sqlalchemy import Column, BigInteger, Date, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .enums import PTOStatusEnum

class EmployeeSickDay(Base):
    """
    ORM model for the 'employee_sickday' table.
    Represents a sick day request by an employee.

    Attributes:
        sickday_id (BigInteger): Primary key for the sick day request.
        emp_id (BigInteger): Foreign key referencing the employee.
        date (Date): Date of the sick day.
        status (Enum): Status of the sick day request (see PTOStatusEnum).
        approved_by_manager_id (BigInteger): Foreign key referencing the approving manager.
        created_at (DateTime): Timestamp when the sick day request was created.
        updated_at (DateTime): Timestamp when the sick day request was last updated.
        # Relationships to employee and manager are defined elsewhere.
    """
    __tablename__ = 'employee_sickday'
    sickday_id = Column(BigInteger, primary_key=True)
    emp_id = Column(BigInteger, ForeignKey('employee.emp_id'))
    date = Column(Date)
    status = Column(Enum(PTOStatusEnum))
    approved_by_manager_id = Column(BigInteger, ForeignKey('manager.manager_id'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    # Relationships (to be completed in employee.py, manager.py)
