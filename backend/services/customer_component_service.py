"""
customer_component_service.py

Service layer for customer component operations.
Provides CRUD operations for customer components using the repository pattern.
All operations are asynchronous and require a database session.
"""

from backend.repository.seller_component_repository import SellerComponentRepository

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
        Retrieve all customer components.
        Returns:
            List of customer components
        """
        return await self.repo.get_all()

    async def get_component(self, id):
        """
        Retrieve a single customer component by ID.
        Args:
            id: Component ID
        Returns:
            Customer component object
        """
        return await self.repo.get_by_id(id)

    async def create_component(self, img_url, description):
        """
        Create a new customer component.
        Args:
            img_url: Image URL
            description: Component description
        Returns:
            Created customer component object
        """
        return await self.repo.create(img_url, description)

    async def update_component(self, id, **kwargs):
        """
        Update a customer component.
        Args:
            id: Component ID
            kwargs: Fields to update
        Returns:
            Updated customer component object
        """
        return await self.repo.update(id, **kwargs)

    async def delete_component(self, id):
        """
        Delete a customer component by ID.
        Args:
            id: Component ID
        Returns:
            Result of deletion
        """
        return await self.repo.delete(id)
