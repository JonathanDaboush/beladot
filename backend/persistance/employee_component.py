
# ------------------------------------------------------------------------------
# employee_component.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the employee_component table.
# This module defines the EmployeeComponent class, which represents a component
# associated with an employee, such as a skill, asset, or responsibility. Each
# component is linked to a department.
# ------------------------------------------------------------------------------

from sqlalchemy import BigInteger, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from backend.persistance.base import Base

class EmployeeComponent(Base):
    """
    ORM model for the 'employee_component' table.
    Represents a component (e.g., skill, asset, responsibility) associated with an employee.

    Attributes:
        id (BigInteger): Primary key for the component.
        img_url (String): URL to an image representing the component.
        description (String): Textual description of the component.
        department_id (Integer): Foreign key referencing the department.
    """
    __tablename__ = 'employee_component'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    img_url: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    department_id: Mapped[int] = mapped_column(Integer, ForeignKey('department.department_id'), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
