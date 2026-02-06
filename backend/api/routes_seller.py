from backend.persistance.db_dependency import get_db
from fastapi import APIRouter, Depends, HTTPException, Request
from backend.schemas.schemas_seller import (
    SellerProductCreate, SellerProductUpdate, SellerProductResponse
)
from backend.services import sellerServices

router = APIRouter(prefix="/api/v1/seller", tags=["seller"])

def require_role(role: str):
    async def dependency(request: Request):
        identity = getattr(request.state, "identity", {})
        if identity.get("role") != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return identity
    return dependency

from typing import Any
async def dummy_seller_service() -> Any:
    class DummyService:
        async def create_product(self, product: Any) -> Any:
            return product
        async def edit_product(self, product_id: int, **kwargs: Any) -> dict[str, Any]:
            return {"id": product_id, **kwargs}
    return DummyService()


@router.post("/products", response_model=SellerProductResponse)
async def create_product(
    product: SellerProductCreate,
    identity: dict[str, Any] = Depends(require_role("seller")),
    db: Any = Depends(get_db),
) -> SellerProductResponse:
    from backend.services.sellerServices import SellerService
    service = SellerService(db)
    result = await service.create_product(product.model_dump())
    return SellerProductResponse(**result)


@router.put("/products/{product_id}", response_model=SellerProductResponse)
async def update_product(
    product_id: int,
    product: SellerProductUpdate,
    identity: dict[str, Any] = Depends(require_role("seller")),
    db: Any = Depends(get_db),
) -> SellerProductResponse:
    from backend.services.sellerServices import SellerService
    service = SellerService(db)
    result = await service.edit_product({'product_id': product_id, **product.model_dump(exclude_unset=True)})
    return SellerProductResponse(**result)
