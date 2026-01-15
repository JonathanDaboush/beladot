
# ------------------------------------------------------------------------------
# enums.py
# ------------------------------------------------------------------------------
# Enumerations for various status and type fields used throughout the persistence
# layer. These enums provide a consistent set of values for statuses such as
# orders, payments, refunds, PTO, and more.
# ------------------------------------------------------------------------------

import enum

# Refund request status (legacy, not used as enum.Enum)
class RefundRequestStatusEnum:
    PENDING = 'pending'
    APPROVED = 'approved'
    DENIED = 'denied'

class SellerStatusEnum(enum.Enum):
    """Status of a seller account."""
    pending = 'pending'
    active = 'active'
    suspended = 'suspended'
    banned = 'banned'

class ShipmentStatusEnum(enum.Enum):
    """Status of a shipment."""
    created = 'created'
    pending = 'pending'
    packed = 'packed'
    shipped = 'shipped'
    in_transit = 'in_transit'
    delivered = 'delivered'
    failed = 'failed'
    returned = 'returned'

class OrderStatusEnum(enum.Enum):
    """Status of an order."""
    pending = 'pending'
    confirmed = 'confirmed'
    shipped = 'shipped'
    delivered = 'delivered'
    cancelled = 'cancelled'
    returned = 'returned'

class PaymentStatusEnum(enum.Enum):
    """Status of a payment."""
    pending = 'pending'
    completed = 'completed'
    failed = 'failed'
    refunded = 'refunded'

class RefundStatusEnum(enum.Enum):
    """Status of a refund."""
    requested = 'requested'
    approved = 'approved'
    rejected = 'rejected'
    processed = 'processed'

class PayoutStatusEnum(enum.Enum):
    """Status of a payout to a seller or employee."""
    pending = 'pending'
    processed = 'processed'
    completed = 'completed'

class PTOStatusEnum(enum.Enum):
    """Status of a paid time off (PTO) request."""
    pending = 'pending'
    approved = 'approved'
    declined = 'declined'

class ShiftStatusEnum(enum.Enum):
    """Status of a work shift."""
    scheduled = 'scheduled'
    completed = 'completed'
    canceled = 'canceled'

class IssueTypeEnum(enum.Enum):
    """Type of issue reported for a shipment or product."""
    damaged = 'damaged'
    lost = 'lost'
    delayed = 'delayed'
    undeliverable = 'undeliverable'

class AccountTypeEnum(enum.Enum):
    cheque = 'cheque'
    credit = 'credit'
