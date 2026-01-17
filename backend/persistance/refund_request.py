
# ------------------------------------------------------------------------------
# refund_request.py
# ------------------------------------------------------------------------------
# ORM entity for refund requests, extending the RefundRequest domain model.
# This module defines the RefundRequestEntity class, which represents a refund
# request in the persistence layer, mapping to the domain model.
# ------------------------------------------------------------------------------

from backend.models.model.refund_request import RefundRequest

class RefundRequestEntity(RefundRequest):
    """
    ORM entity for refund requests, extending the RefundRequest domain model.

    Attributes:
        refund_request_id: Unique identifier for the refund request.
        order_id: Associated order ID.
        order_item_ids: List of order item IDs included in the refund.
        reason: Reason for the refund request.
        status: Status of the refund request.
        date_of_request: Date the refund was requested (optional).
        description: Additional description or notes (optional).
    """
    def __init__(self, refund_request_id, order_id, order_item_ids, reason, status, date_of_request=None, description=None):
        super().__init__(refund_request_id, order_id, order_item_ids, reason, status, date_of_request, description)
