
import sys
import os
import pytest
# Ensure backend is importable when running from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from backend.models.model.refund_request import RefundRequest

def test_refund_request_description():
    refund = RefundRequest(
        refund_request_id=1,
        order_id=10,
        order_item_ids=[100, 101],
        reason="Damaged item",
        status="pending",
        description="Customer reported item was broken on arrival."
    )
    assert refund.description == "Customer reported item was broken on arrival."
    assert refund.reason == "Damaged item"
    assert refund.status == "pending"
