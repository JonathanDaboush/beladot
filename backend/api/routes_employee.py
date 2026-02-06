from backend.persistance.db_dependency import get_db
from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from backend.schemas.schemas_employee import (
    EmployeeComponentCreate, EmployeeComponentResponse
)

router = APIRouter(prefix="/api/v1/employee", tags=["employee"])

def require_role(role: str):
    async def dependency(request: Request):
        identity = getattr(request.state, "identity", {})
        if identity.get("role") != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return identity
    return dependency

from typing import Any
from backend.schemas.schemas_employee import EmployeeComponentCreate, EmployeeComponentResponse
from sqlalchemy.ext.asyncio import AsyncSession

async def dummy_employee_service() -> Any:
    class DummyService:
        async def get_all_employee_components(self, employee_id: int, db: AsyncSession) -> list[EmployeeComponentResponse]:
            return []
        async def create_employee_component(self, employee_id: int, db: AsyncSession, **kwargs: Any) -> EmployeeComponentResponse:
            payload: dict[str, Any] = {**kwargs}
            payload.setdefault('id', 1)
            return EmployeeComponentResponse(**payload)
    return DummyService()



@router.get("/components", response_model=List[EmployeeComponentResponse])
async def get_all_employee_components(
    employeeService: Any = Depends(dummy_employee_service),
    identity: dict[str, Any] = Depends(require_role("employee")),
    db: AsyncSession = Depends(get_db),
) -> list[EmployeeComponentResponse]:
    return await employeeService.get_all_employee_components(employee_id=identity["employee_id"], db=db)



@router.post("/components", response_model=EmployeeComponentResponse)
async def create_employee_component(
    component: EmployeeComponentCreate,
    employeeService: Any = Depends(dummy_employee_service),
    identity: dict[str, Any] = Depends(require_role("employee")),
    db: AsyncSession = Depends(get_db),
) -> EmployeeComponentResponse:
    return await employeeService.create_employee_component(employee_id=identity["employee_id"], db=db, **component.model_dump())
