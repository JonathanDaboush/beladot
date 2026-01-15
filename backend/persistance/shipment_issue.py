"""
shipment_issue.py

SQLAlchemy ORM model for the shipment_issue table.
Represents an issue related to a shipment, including type, description, and appointment.
"""

from sqlalchemy import Column, BigInteger, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .enums import IssueTypeEnum

class ShipmentIssue(Base):
    __tablename__ = 'shipment_issue'
    issue_id = Column(BigInteger, primary_key=True)
    shipment_id = Column(BigInteger, ForeignKey('shipment.shipment_id'))
    shipment_employee_name = Column(String(255))
    issue_type = Column(Enum(IssueTypeEnum))
    description = Column(Text)
    created_at = Column(DateTime)
    appointted_to = Column(String(255))  # New field for appointed to
    # Relationships (to be completed in shipment.py)
