
from fastapi import APIRouter, Depends, HTTPException, Request
from backend.services.managerServices import ManagerService
from pydantic import BaseModel
from typing import Optional
from backend.schemas.schemas_incident import IncidentCreate as IncidentCreateRequest
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from backend.persistance.async_base import AsyncSessionLocal

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

router = APIRouter(prefix="/api/v1/manager", tags=["manager"])

def require_role(role: str):
    async def dependency(request: Request):
        identity = getattr(request.state, "identity", {})
        role_val = identity.get("role")
        if role_val is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if role_val != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return identity
    return dependency

class EmployeeEditRequest(BaseModel):
    notes: Optional[str] = None

# Dependency for DB session (replace with your actual DB dependency)




@router.post("/incident", response_model=Any)
async def create_incident_report(
    payload: IncidentCreateRequest,
    identity: dict[str, Any] = Depends(require_role("manager")),
    db: AsyncSession = Depends(get_db)
) -> Any:
    service = ManagerService(db)
    return await service.create_incident_report(
        manager_id=identity["manager_id"],
        employee_id=payload.employee_id,
        description=payload.description,
        cost=payload.cost,
        date=payload.date
    )


@router.put("/employee/{employee_id}", response_model=Any)
async def edit_employee_info(
    employee_id: int,
    payload: EmployeeEditRequest,
    identity: dict[str, Any] = Depends(require_role("manager")),
    db: AsyncSession = Depends(get_db)
) -> Any:
    service = ManagerService(db)
    return await service.edit_employee_info(
        manager_id=identity["manager_id"],
        employee_id=employee_id,
        **payload.model_dump()
    )
