
# ------------------------------------------------------------------------------
# customer_shipment.py
# ------------------------------------------------------------------------------
# SQLAlchemy ORM model for the customer_shipment table.
# This module defines the CustomerShipment class, which represents a shipment
# associated with a customer. Stores address and shipment details for the user.
# ------------------------------------------------------------------------------

from typing import Optional
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class CustomerShipment(Base):
    """
    ORM model for the 'customer_shipment' table.
    Represents a shipment associated with a customer, including address details.

    Attributes:
        cs_id (BigInteger): Primary key for the customer shipment.
        customer_id (BigInteger): Foreign key referencing the user (customer).
        address (String): Full address string (may be deprecated in favor of structured fields).
        postal_code (String): Postal or ZIP code for the shipment address.
        street_line_1 (String): First line of the street address.
        street_line_2 (String): Second line of the street address (optional).
        city (String): City of the shipment address.
        state_province (String): State or province of the shipment address.
        country (String): Country of the shipment address.
        # Relationship to user is defined elsewhere.
    """
    __tablename__ = 'customer_shipment'
    cs_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    customer_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.user_id'))
    address: Mapped[str] = mapped_column(String(255))
    postal_code: Mapped[str] = mapped_column(String(20))
    street_line_1: Mapped[str] = mapped_column(String(255))
    street_line_2: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    city: Mapped[str] = mapped_column(String(100))
    state_province: Mapped[str] = mapped_column(String(100))
    country: Mapped[str] = mapped_column(String(100))
    # Relationship (to be completed in user.py)
