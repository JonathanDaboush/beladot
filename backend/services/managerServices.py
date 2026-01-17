from backend.repositories.repository.incident_repository import IncidentRepository
from backend.repositories.repository.employee_repository import EmployeeRepository
from backend.repositories.repository.shift_repository import ShiftRepository
from backend.repositories.repository.employee_pto_repository import EmployeePTORepository
from backend.repositories.repository.employee_sickday_repository import EmployeeSickDayRepository
from backend.models.model.incident import Incident
from backend.models.model.shift import Shift
from backend.models.model.employee_pto import EmployeePTO
from backend.models.model.employee_sickday import EmployeeSickDay
from sqlalchemy.ext.asyncio import AsyncSession

class ManagerService:
    """
    Service layer for manager operations, including incident, PTO, and sick day management.
    Provides CRUD operations for incidents and editing PTO/sick day info.
    """
    def __init__(self, db: AsyncSession):
        self.db = db
        self.incident_repo = IncidentRepository(db)
        self.employee_repo = EmployeeRepository(db)
        self.shift_repo = ShiftRepository(db)
        self.pto_repo = EmployeePTORepository(db)
        self.sickday_repo = EmployeeSickDayRepository(db)
        from backend.repositories.repository.manager_repository import ManagerRepository
        self.manager_repo = ManagerRepository(db)

    # Incident CRUD
    async def create_incident_report(self, manager_id, employee_id, description, cost, date=None):
        """
        Create a new incident report for an employee.
        Args:
            manager_id: ID of the manager
            employee_id: ID of the employee
            description: Incident description
            cost: Cost associated with the incident
            date: Date of the incident
        Returns:
            Incident object or None if not allowed
        """
        employee = await self.employee_repo.get_by_id(employee_id)
        # Optionally, validate manager permissions here
        manager = await self.manager_repo.get_by_id(manager_id)
        if not employee or not manager or employee.department_id != manager.department_id:
            return None  # Not allowed
        incident = Incident(
            incident_id=None,
            employee_id=employee_id,
            description=description,
            cost=cost,
            date=date,
            status_addressed=False,
            paid_all=False
        )
        await self.incident_repo.save(incident)
        return incident

    async def edit_incident_report(self, incident_id, **kwargs):
        """
        Edit an existing incident report.
        Args:
            incident_id: ID of the incident
            kwargs: Fields to update
        Returns:
            Updated incident object
        """
        return await self.incident_repo.update(incident_id, **kwargs)

    async def delete_incident_report(self, incident_id):
        """
        Delete an incident report by ID.
        Args:
            incident_id: ID of the incident
        Returns:
            Result of deletion
        """
        return await self.incident_repo.delete(incident_id)

    async def get_incident_report(self, incident_id):
        """
        Get a single incident report by ID.
        Args:
            incident_id: ID of the incident
        Returns:
            Incident object
        """
        return await self.incident_repo.get_by_id(incident_id)

    async def get_all_incident_reports(self):
        """
        Get all incident reports.
        Returns:
            List of Incident objects
        """
        return await self.incident_repo.get_all()

    async def edit_pto_info(self, pto_id, **kwargs):
        """
        Edit PTO information for an employee.
        Args:
            pto_id: PTO request ID
            kwargs: Fields to update
        Returns:
            Updated PTO object or None
        """
        pto = await self.pto_repo.get_by_id(pto_id)
        if not pto:
            return None
        await self.pto_repo.update(pto_id, **kwargs)
        return await self.pto_repo.get_by_id(pto_id)

    async def edit_sickday_info(self, sickday_id, **kwargs):
        """
        Edit sick day information for an employee.
        Args:
            sickday_id: Sick day request ID
            kwargs: Fields to update
        Returns:
            Updated sick day object or None
        """
        sickday = await self.sickday_repo.get_by_id(sickday_id)
        if not sickday:
            return None
        await self.sickday_repo.update(sickday_id, **kwargs)
        return await self.sickday_repo.get_by_id(sickday_id)

    async def edit_employee_info(self, manager_id, employee_id, **kwargs):
        employee = await self.employee_repo.get_by_id(employee_id)
        if not employee:
            return None
        manager = await self.manager_repo.get_by_id(manager_id)
        if not manager or employee.department_id != manager.department_id:
            return None
        await self.employee_repo.update(employee_id, **kwargs)
        return await self.employee_repo.get_by_id(employee_id)
