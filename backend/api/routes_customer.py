from backend.persistance.db_dependency import get_db
from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Any
from backend.schemas.schemas_customer import (
    CartItemAdd, CartItemResponse, WishlistItemAdd, WishlistItemResponse
)

router = APIRouter(prefix="/api/v1/customer", tags=["customer"])

def require_role(role: str):
    async def dependency(request: Request):
        identity = getattr(request.state, "identity", {})
        if identity.get("role") != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return identity
    return dependency

from backend.services.customerServices import add_item_to_cart, add_item_to_wishlist

@router.post("/cart/items", response_model=CartItemResponse)
async def add_item_to_cart_route(
    item: CartItemAdd,
    identity: dict[str, Any] = Depends(require_role("user")),
    db: Any = Depends(get_db),
) -> CartItemResponse:
    result = await add_item_to_cart(
        user_id=identity["user_id"],
        product_id=item.product_id,
        quantity=item.quantity,
        db=db
    )
    return CartItemResponse(**result)

@router.post("/wishlist/items", response_model=WishlistItemResponse)
async def add_item_to_wishlist_route(
    item: WishlistItemAdd,
    identity: dict[str, Any] = Depends(require_role("user")),
    db: Any = Depends(get_db),
) -> WishlistItemResponse:
    wishlist_item = await add_item_to_wishlist(
        user_id=identity["user_id"],
        product_id=item.product_id,
        quantity=getattr(item, "quantity", 1),
        db=db
    )
    return WishlistItemResponse(
        id=int(getattr(wishlist_item, "wishlist_item_id", -1)),
        product_id=wishlist_item.product_id,
        user_id=wishlist_item.user_id,
    )
