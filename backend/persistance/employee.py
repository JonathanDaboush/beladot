
# ------------------------------------------------------------------------------
# employee.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the employee table.
# This module defines the Employee class, which represents an employee in the
# organization. Each employee is associated with a user and a department.
# Relationships to PTO, sick days, shifts, and payments are defined elsewhere.
# ------------------------------------------------------------------------------

from sqlalchemy import BigInteger, ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Employee(Base):
    name: str = ''
    """
    ORM model for the 'employee' table.
    Represents an employee in the organization.

    Attributes:
        emp_id (BigInteger): Primary key for the employee.
        user_id (BigInteger): Foreign key referencing the user.
        department_id (BigInteger): Foreign key referencing the department.
        # Relationships to PTO, sick days, shifts, and payments are defined elsewhere.
    """
    __tablename__ = 'employee'
    emp_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.user_id'))
    department_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('department.department_id'))
    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)  # Temporary field for update testing
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

# Relationships (to be completed in employee_pto.py, employee_sickday.py, shift.py, shift_request.py, finance_employee.py, employee_payment.py)
