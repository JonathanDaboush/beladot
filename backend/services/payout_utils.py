from backend.model.refund import Refund
from backend.model.seller_payout import SellerPayout
from backend.model.reimbursement import Reimbursement
from backend.repository.refund_repository import RefundRepository
from backend.repository.seller_payout_repository import SellerPayoutRepository
from backend.repository.reimbursement_repository import ReimbursementRepository
from datetime import datetime

async def create_refund(db, payment_id, order_item_id, amount, reason, approved_by_cs_id, status):
    """
    Create a refund record and save it to the database.
    Args:
        db: Database session
        payment_id: Payment ID
        order_item_id: Order item ID
        amount: Refund amount
        reason: Reason for refund
        approved_by_cs_id: Customer service approver ID
        status: Refund status
    Returns:
        Saved Refund object
    """
    refund = Refund(
        refund_id=None,  # Assume autoincrement
        payment_id=payment_id,
        order_item_id=order_item_id,
        amount=amount,
        reason=reason,
        approved_by_cs_id=approved_by_cs_id,
        status=status,
        created_at=datetime.now(),
        processed_at=None
    )
    repo = RefundRepository(db)
    return await repo.save(refund)
async def create_seller_payout(db, seller_id, amount, currency, status='pending'):
    """
    Create a seller payout record and save it to the database.
    Args:
                db: Database session
                seller_id: Seller ID
                amount: Payout amount
                currency: Currency code
                status: Payout status (default 'pending')
            Returns:
                Saved SellerPayout object
            """
    payout = SellerPayout(
        payout_id=None,  # Assume autoincrement
        seller_id=seller_id,
        amount=amount,
        currency=currency,
        date_of_payment=None,
        status=status,
        created_at=datetime.now()
    )
    repo = SellerPayoutRepository(db)
    return await repo.save(payout)
async def create_reimbursement(db, employee_id, incident_id, description, amount_approved, status=True):
    """
    Create a reimbursement record and save it to the database.
    Args:
        db: Database session
        employee_id: Employee ID
                incident_id: Incident ID
                description: Description of reimbursement
                amount_approved: Approved amount
                status: Reimbursement status (default True)
            Returns:
                Saved Reimbursement object
            """
    reimbursement = Reimbursement(
        reimbursement_id=None,  # Assume autoincrement
        employee_id=employee_id,
        incident_id=incident_id,
        description=description,
        response=None,
        amount_approved=amount_approved,
        status=status,
        status_addressed=True,
        paid_all=False
    )
    repo = ReimbursementRepository(db)
    return await repo.save(reimbursement)
