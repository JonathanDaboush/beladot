"""
shipment_issue.py

SQLAlchemy ORM model for the shipment_issue table.
Represents an issue related to a shipment, including type, description, and appointment.
"""


from __future__ import annotations

from typing import Optional
import datetime
from sqlalchemy import BigInteger, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .enums import IssueTypeEnum


class ShipmentIssue(Base):
    __tablename__ = 'shipment_issue'
    issue_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    shipment_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('shipment.shipment_id'))
    shipment_employee_name: Mapped[str] = mapped_column(String(255))
    issue_type: Mapped[IssueTypeEnum] = mapped_column(Enum(IssueTypeEnum))
    description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    appointted_to: Mapped[str] = mapped_column(String(255))  # New field for appointed to
    # Relationships (to be completed in shipment.py)
