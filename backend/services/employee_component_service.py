from backend.repository.employee_component_repository import EmployeeComponentRepository

"""
employee_component_service.py

Service layer for employee component operations.
Provides CRUD operations for employee components using the repository pattern.
All operations are asynchronous and require a database session.
"""

class EmployeeComponentService:
    def __init__(self, repo: EmployeeComponentRepository):
        """
        Initialize EmployeeComponentService with repository.
        Args:
            repo: EmployeeComponentRepository instance
        """
        self.repo = repo

    async def get_all_components(self):
        """
        Retrieve all employee components.
        Returns:
            List of employee components
        """
        return await self.repo.get_all()

    async def get_components_for_employee(self, employee):
        """
        Retrieve employee components for a specific employee's department.
        Args:
            employee: Employee object (must have department_id)
        Returns:
            List of employee components
        """
        return await self.repo.get_by_department(employee.department_id)

    async def get_component(self, id):
        """
        Retrieve a single employee component by ID.
        Args:
            id: Component ID
        Returns:
            Employee component object
        """
        return await self.repo.get_by_id(id)

    async def create_component(self, img_url, description, department_id):
        """
        Create a new employee component.
        Args:
            img_url: Image URL
            description: Component description
            department_id: Department ID
        Returns:
            Created employee component object
        """
        return await self.repo.create(img_url, description, department_id)

    async def update_component(self, id, **kwargs):
        """
        Update an employee component.
        Args:
            id: Component ID
            kwargs: Fields to update
        Returns:
            Updated employee component object
        """
        return await self.repo.update(id, **kwargs)

    async def delete_component(self, id):
        """
        Delete an employee component by ID.
        Args:
            id: Component ID
        Returns:
            Result of deletion
        """
        return await self.repo.delete(id)
