from backend.persistance.db_dependency import get_db
from fastapi import APIRouter, Depends, HTTPException, Request
from backend.schemas.schemas_shipping import (
    ShipmentCreate, ShipmentResponse, ShipmentEventCreate, ShipmentEventResponse
)
from backend.services import shippingServices

router = APIRouter(prefix="/api/v1/shipping", tags=["shipping"])

def require_role(role: str):
    async def dependency(request: Request):
        identity = getattr(request.state, "identity", {})
        # Shipping endpoints restricted to employees only
        if identity.get("role") != "employee":
            raise HTTPException(status_code=403, detail="Forbidden")
        return identity
    return dependency

from typing import Any
async def dummy_shipping_service() -> Any:
    class DummyService:
        async def create_shipment(self, **kwargs: Any) -> dict[str, Any]:
            return kwargs
        async def create_shipment_event(self, **kwargs: Any) -> dict[str, Any]:
            return kwargs
    return DummyService()


@router.post("/shipments", response_model=ShipmentResponse)
async def create_shipment(
    shipment: ShipmentCreate,
    identity: dict[str, Any] = Depends(require_role("employee")),
    db: Any = Depends(get_db),
) -> ShipmentResponse:
    result = await shippingServices.create_shipment(employee_id=identity["employee_id"], db=db, **shipment.model_dump())
    return ShipmentResponse(**result)


@router.post("/shipment-events", response_model=ShipmentEventResponse)
async def create_shipment_event(
    event: ShipmentEventCreate,
    identity: dict[str, Any] = Depends(require_role("employee")),
    db: Any = Depends(get_db),
) -> ShipmentEventResponse:
    result = await shippingServices.create_shipment_event(db=db, **event.model_dump())
    if isinstance(result, dict):
        return ShipmentEventResponse(
            id=result.get('id', 0),
            shipment_id=result.get('shipment_id', 0),
            event_type=result.get('event_type', 'picked_up')  # type: ignore
        )
    # Return a default response if result is not as expected
    return ShipmentEventResponse(
        id=0,
        shipment_id=0,
        event_type='picked_up'  # type: ignore
    )
