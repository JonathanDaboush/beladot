from backend.services.employee_component_service import EmployeeComponentService
from backend.services.seller_component_service import SellerComponentService
from backend.repositories.repository.employee_component_repository import EmployeeComponentRepository
from backend.repositories.repository.seller_component_repository import SellerComponentRepository

"""
managementServices.py

Service layer for managing employee and seller components.
Provides CRUD operations for both employee and seller components using their respective services and repositories.
All operations are asynchronous and require a database session.
"""

from sqlalchemy.ext.asyncio import AsyncSession

class ManagementServices:
    def __init__(self, db: AsyncSession):
        """
        Initialize ManagementServices with database session.
        Args:
            db: Database session
        """
        self.employee_component_service = EmployeeComponentService(EmployeeComponentRepository(db))
        self.seller_component_service = SellerComponentService(SellerComponentRepository(db))

    # Employee Component CRUD
    async def get_all_employee_components(self):
        """
        Retrieve all employee components.
        Returns:
            List of employee components
        """
        return await self.employee_component_service.get_all_components()

    async def get_employee_components_for_employee(self, employee):
        """
        Retrieve employee components for a specific employee.
        Args:
            employee: Employee object
        Returns:
            List of employee components
        """
        return await self.employee_component_service.get_components_for_employee(employee)

    async def get_employee_component(self, id):
        """
        Retrieve a single employee component by ID.
        Args:
            id: Component ID
        Returns:
            Employee component object
        """
        return await self.employee_component_service.get_component(id)

    async def create_employee_component(self, img_url, description, department_id):
        """
        Create a new employee component.
        Args:
            img_url: Image URL
            description: Component description
            department_id: Department ID
        Returns:
            Created employee component object
        """
        return await self.employee_component_service.create_component(img_url, description, department_id)

    async def update_employee_component(self, id, **kwargs):
        """
        Update an employee component.
        Args:
            id: Component ID
            kwargs: Fields to update
        Returns:
            Updated employee component object
        """
        return await self.employee_component_service.update_component(id, **kwargs)

    async def delete_employee_component(self, id):
        """
        Delete an employee component by ID.
        Args:
            id: Component ID
        Returns:
            Result of deletion
        """
        return await self.employee_component_service.delete_component(id)

    # Seller Component CRUD
    async def get_all_seller_components(self):
        """
        Retrieve all seller components.
        Returns:
            List of seller components
        """
        return await self.seller_component_service.get_all_components()

    async def get_seller_component(self, id):
        """
        Retrieve a single seller component by ID.
        Args:
            id: Component ID
        Returns:
            Seller component object
        """
        return await self.seller_component_service.get_component(id)

    async def create_seller_component(self, img_url, description):
        """
        Create a new seller component.
        Args:
            img_url: Image URL
            description: Component description
        Returns:
            Created seller component object
        """
        return await self.seller_component_service.create_component(img_url, description)

    async def update_seller_component(self, id, **kwargs):
        """
        Update a seller component.
        Args:
            id: Component ID
            kwargs: Fields to update
        Returns:
            Updated seller component object
        """
        return await self.seller_component_service.update_component(id, **kwargs)

    async def delete_seller_component(self, id):
        """
        Delete a seller component by ID.
        Args:
            id: Component ID
        Returns:
            Result of deletion
        """
        return await self.seller_component_service.delete_component(id)
