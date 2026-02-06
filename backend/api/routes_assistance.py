from backend.persistance.db_dependency import get_db
from fastapi import APIRouter, Depends, HTTPException, Request
from backend.schemas.schemas_assistance import (
    AssistanceRefundStatusEmail, AssistanceRefundStatusResponse,
    AssistanceComplaint, AssistanceComplaintResponse
)
from backend.services import customerAssistanceServices

router = APIRouter(prefix="/api/v1/assistance", tags=["assistance"])

# Role enforcement
def require_role(role: str):
    async def dependency(request: Request):
        identity = getattr(request.state, "identity", {})
        if identity.get("role") != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return identity
    return dependency

# Dummy service for tests / startup
from typing import Any, Dict

async def dummy_assistance_service():
    class DummyService:
        async def send_customer_refund_status_email(self, **kwargs: Any) -> Dict[str, Any]:
            return kwargs

        async def process_customer_complaint(self, **kwargs: Any) -> Dict[str, Any]:
            return kwargs

    return DummyService()

@router.post("/refund-status", response_model=AssistanceRefundStatusResponse)
async def send_refund_status_email(
    payload: AssistanceRefundStatusEmail,
    identity: dict = Depends(require_role("user")),
    db: Any = Depends(get_db),
):
    result = await customerAssistanceServices.send_customer_refund_status_email(user_id=identity["user_id"], db=db, **payload.model_dump())
    return {"result": result}

@router.post("/complaint", response_model=AssistanceComplaintResponse)
async def process_complaint(
    complaint: AssistanceComplaint,
    identity: dict = Depends(require_role("user")),
    db: Any = Depends(get_db),
):
    result = await customerAssistanceServices.process_customer_complaint(user_id=identity["user_id"], db=db, **complaint.model_dump())
    return {"result": result}
