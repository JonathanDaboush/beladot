
# ------------------------------------------------------------------------------
# employee_component.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the employee_component table.
# This module defines the EmployeeComponent class, which represents a component
# associated with an employee, such as a skill, asset, or responsibility. Each
# component is linked to a department.
# ------------------------------------------------------------------------------

from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey
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
    id = Column(BigInteger, primary_key=True)
    img_url = Column(String(255))
    description = Column(String(255))
    department_id = Column(Integer, ForeignKey('department.department_id'), nullable=False)
