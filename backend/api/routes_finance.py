
from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List

from backend.schemas.schemas import (
    FinanceIssueCreate,
    FinanceIssueUpdate,
    FinanceIssueResponse,
    FinanceReimbursementUpdate,
    FinanceReimbursementResponse,
)

router = APIRouter(prefix="/api/finance", tags=["finance"])

# -------------------------------------------------
# Dependency: Role enforcement (request-scoped)
# -------------------------------------------------
def require_role(role: str):
    async def dependency(request: Request):
        identity = getattr(request.state, "identity", {})
        current_role = identity.get("role")
        if current_role is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if current_role != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return identity
    return dependency

# -------------------------------------------------
# Dummy finance service (IMPORT-SAFE)
# -------------------------------------------------
from typing import Any
class DummyFinanceService:
    async def get_issues_catalog(self, employee_id: int) -> list[Any]:
        return []

    async def create_issue(self, employee_id: int, **kwargs: Any) -> dict[str, Any]:
        return {**kwargs, "id": 1}

    async def update_issue(self, issue_id: int, **kwargs: Any) -> dict[str, Any]:
        return {**kwargs, "id": issue_id}

    async def delete_issue(self, issue_id: int) -> dict[str, Any]:
        return {"id": issue_id, "deleted": True}

async def get_finance_services():
    return DummyFinanceService()

# -------------------------------------------------
# Routes
# -------------------------------------------------

@router.get("/issues", response_model=List[FinanceIssueResponse])
async def get_issues(
    finance_services: DummyFinanceService = Depends(get_finance_services),
    identity: dict[str, Any] = Depends(require_role("employee")),
) -> list[Any]:
    return await finance_services.get_issues_catalog(
        employee_id=identity["employee_id"]
    )

@router.post("/issues", response_model=FinanceIssueResponse)
async def create_issue(
    issue: FinanceIssueCreate,
    finance_services: DummyFinanceService = Depends(get_finance_services),
    identity: dict[str, Any] = Depends(require_role("employee")),
) -> dict[str, Any]:
    return await finance_services.create_issue(
        employee_id=identity["employee_id"],
        **issue.model_dump(),
    )

@router.put("/issues/{issue_id}", response_model=FinanceIssueResponse)
async def update_issue(
    issue_id: int,
    update: FinanceIssueUpdate,
    finance_services: DummyFinanceService = Depends(get_finance_services),
    identity: dict[str, Any] = Depends(require_role("employee")),
) -> dict[str, Any]:
    return await finance_services.update_issue(
        issue_id,
        **update.model_dump(),
    )

@router.delete("/issues/{issue_id}")
async def delete_issue(
    issue_id: int,
    finance_services: DummyFinanceService = Depends(get_finance_services),
    identity: dict[str, Any] = Depends(require_role("employee")),
) -> dict[str, Any]:
    return await finance_services.delete_issue(issue_id)

@router.put(
    "/reimbursements/{reimbursement_id}",
    response_model=FinanceReimbursementResponse,
)
async def update_reimbursement(
    reimbursement_id: int,
    update: FinanceReimbursementUpdate,
    finance_services: DummyFinanceService = Depends(get_finance_services),
    identity: dict[str, Any] = Depends(require_role("employee")),
) -> dict[str, Any]:
    return {**update.model_dump(), "id": reimbursement_id}

