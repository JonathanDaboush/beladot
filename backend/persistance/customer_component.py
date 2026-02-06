
# ------------------------------------------------------------------------------
# customer_component.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the customer_component table.
# This module defines the CustomerComponent class, which represents a component
# associated with a customer in the database. Each component has an image URL
# and a description. This file is part of the persistence layer and is used by
# the repository and service layers for CRUD operations.
# ------------------------------------------------------------------------------

from __future__ import annotations

from typing import Any
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from backend.db.base import Base

class CustomerComponent(Base):
    """
    ORM model for the 'customer_component' table.
    Represents a component (e.g., a preference or saved configuration) associated with a customer.

    Attributes:
        id (Integer): Primary key for the component.
        img_url (String): URL to an image representing the component.
        description (String): Textual description of the component.
    """
    __tablename__ = 'customer_component'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    img_url: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
