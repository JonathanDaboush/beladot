
# ------------------------------------------------------------------------------
# payment_service_mock.py
# ------------------------------------------------------------------------------
# Mock implementation of a payment service for testing and development.
# No real financial transactions are performed by this class.
# ------------------------------------------------------------------------------

from typing import Any

class PaymentServiceMock:
    """
    Mock payment service for development/testing.
    Simulates payment and refund operations without real transactions.
    """
    def process_payment(self, *args: Any, **kwargs: Any) -> dict[str, str]:
        """Simulate processing a payment (no real transaction)."""
        return {'status': 'mocked', 'message': 'No real transaction performed.'}

    def refund_payment(self, *args: Any, **kwargs: Any) -> dict[str, str]:
        """Simulate refunding a payment (no real refund)."""
        return {'status': 'mocked', 'message': 'No real refund performed.'}
