from backend.repository.seller_component_repository import SellerComponentRepository

"""
seller_component_service.py

Service layer for seller component operations.
Provides CRUD operations for seller components using the repository pattern.
All operations are asynchronous and require a database session.
"""

class SellerComponentService:
    def __init__(self, repo: SellerComponentRepository):
        """
        Initialize SellerComponentService with repository.
        Args:
            repo: SellerComponentRepository instance
        """
        self.repo = repo

    async def get_all_components(self):
        """
        Retrieve all seller components.
        Returns:
            List of seller components
        """
        return await self.repo.get_all()

    async def get_component(self, id):
        """
        Retrieve a single seller component by ID.
        Args:
            id: Component ID
        Returns:
            Seller component object
        """
        return await self.repo.get_by_id(id)

    async def create_component(self, img_url, description):
        """
        Create a new seller component.
        Args:
            img_url: Image URL
            description: Component description
        Returns:
            Created seller component object
        """
        return await self.repo.create(img_url, description)

    async def update_component(self, id, **kwargs):
        """
        Update a seller component.
        Args:
            id: Component ID
            kwargs: Fields to update
        Returns:
            Updated seller component object
        """
        return await self.repo.update(id, **kwargs)

    async def delete_component(self, id):
        """
        Delete a seller component by ID.
        Args:
            id: Component ID
        Returns:
            Result of deletion
        """
        return await self.repo.delete(id)
