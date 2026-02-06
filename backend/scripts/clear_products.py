
from sqlalchemy import delete
from backend.persistance.async_base import AsyncSessionLocal
# Import models with FKs to product that should be cleared first
from backend.persistance.cart_item import CartItem
from backend.persistance.wishlist_item import WishlistItem
from backend.persistance.shipment_item import ShipmentItem
from backend.persistance.order_item import OrderItem
from backend.persistance.product_comment import ProductComment
from backend.persistance.product_variant_image import ProductVariantImage
from backend.persistance.product_image import ProductImage
from backend.persistance.product_review import ProductReview
from backend.persistance.product_rating import ProductRating
from backend.persistance.product_variant import ProductVariant
from backend.persistance.product import Product



import asyncio

async def main() -> None:
    async with AsyncSessionLocal() as session:
        async def try_delete(model):
            try:
                await session.execute(delete(model))
            except Exception as e:
                if 'does not exist' in str(e) or 'UndefinedTable' in str(e):
                    print(f"Skipping missing table: {getattr(model, '__tablename__', model)}")
                else:
                    raise

        # Delete dependents first to satisfy FKs
        await try_delete(CartItem)
        await try_delete(WishlistItem)
        await try_delete(ShipmentItem)
        await try_delete(OrderItem)
        await try_delete(ProductComment)
        await try_delete(ProductVariantImage)
        await try_delete(ProductImage)
        await try_delete(ProductReview)
        await try_delete(ProductRating)
        await try_delete(ProductVariant)
        await try_delete(Product)
        await session.commit()
    print("Purged all products and related records.")

if __name__ == "__main__":
    asyncio.run(main())
