
"""
employeeServices.py

Service layer for employee operations, including reimbursements, shifts, PTO, sick days, and email notifications.
All repository/model operations use a request-scoped DB session managed by the caller.
All methods are asynchronous and provide detailed employee-related business logic.
"""

from backend.persistance.reimbursement import Reimbursement
from backend.repository.employee_repository import EmployeeRepository
from backend.repository.shift_repository import ShiftRepository
from backend.repository.employee_pto_repository import EmployeePTORepository
from backend.repository.employee_sickday_repository import EmployeeSickDayRepository
from backend.persistance.shift import Shift
from backend.persistance.employee_pto import EmployeePTO
from backend.persistance.employee_sickday import EmployeeSickDay
from backend.repository.reimbursement_repository import ReimbursementRepository

from backend.services.interfaces.employee_service_interface import IEmployeeService

class EmployeeService(IEmployeeService):
    """
    Service class for employee-related operations.
    Handles reimbursements, shifts, PTO, sick days, and notifications.
    """

    async def get_reimbursement_details(self, reimbursement_id):
        reimbursement_repo = ReimbursementRepository(self.db)
        incident_repo = IncidentRepository(self.db)
        employee_repo = EmployeeRepository(self.db)
        finance_employee_repo = FinanceEmployeeRepository(self.db)

        reimbursement = await reimbursement_repo.get_by_id(reimbursement_id)
        if not reimbursement:
            return None
        incident = await incident_repo.get_by_id(reimbursement.incident_id) if reimbursement.incident_id else None
        employee = None
        if incident and hasattr(incident, 'employee_id'):
            employee = await employee_repo.get_by_id(incident.employee_id)
        finance_employee = None
        if hasattr(reimbursement, 'finance_emp_id') and reimbursement.finance_emp_id:
            finance_employee = await finance_employee_repo.get_by_id(reimbursement.finance_emp_id)
        return {
            'reimbursement_id': getattr(reimbursement, 'reimbursement_id', None),
            'incident_id': getattr(incident, 'incident_id', None) if incident else None,
            'employee_name': getattr(employee, 'name', None) if employee else None,
            'finance_employee_id': getattr(finance_employee, 'id', None) if finance_employee else None
        }

    async def create_reimbursement_claim(self, incident_id, description, amount_requested=None, paystub_url=None):
        reimbursement_repo = ReimbursementRepository(self.db)
        incident_repo = IncidentRepository(self.db)
        employee_repo = EmployeeRepository(self.db)
        incident = await incident_repo.get_by_id(incident_id)
        employee = None
        if incident and hasattr(incident, 'employee_id'):
            employee = await employee_repo.get_by_id(incident.employee_id)
        reimbursement = Reimbursement(
            reimbursement_id=None,
            incident_id=incident_id,
            description=description,
            response=None,
            amount_approved=amount_requested,
            status=False
        )
        await reimbursement_repo.save(reimbursement)
        # Side effect: email sending should be handled by a separate notification service
        return {'reimbursement_id': getattr(reimbursement, 'reimbursement_id', None)}
    def __init__(self, db):
        """
        Args:
            db: SQLAlchemy session (request-scoped, not global; managed by caller).
        """
        self.db = db
        self.employee_repo = EmployeeRepository(db)
        self.shift_repo = ShiftRepository(db)
        self.pto_repo = EmployeePTORepository(db)
        self.sickday_repo = EmployeeSickDayRepository(db)

    async def book_shift(self, employee_id, shift_id=None, start_time=None, end_time=None, department_id=None, created_by_manager_id=None, status=None):
        """
        Book a shift for an employee. Uses class for business logic, model for structure, repository for DB bridge.
        Args:
            employee_id (int): Employee ID booking the shift.
            shift_id (int, optional): Shift ID if updating.
            start_time (datetime): Shift start time.
            end_time (datetime): Shift end time.
            department_id (int, optional): Department ID.
            created_by_manager_id (int, optional): Manager ID who created the shift.
            status (str, optional): Status of the shift.
        """
        # Fetch employee to get department if not provided
        employee = await self.employee_repo.get_by_id(employee_id)
        if not employee:
            return {'error': 'Employee not found'}
        if department_id is None:
            department_id = getattr(employee, 'department_id', None)

        # Load the shift by ID to get times
        shift = None
        if shift_id is not None:
            shift = await self.shift_repo.get_by_id(shift_id)
            if not shift:
                from fastapi import HTTPException
                raise HTTPException(status_code=404, detail="Shift not found")
            start_time = shift.start_time
            end_time = shift.end_time

        # Defensive: ensure times are not None
        if start_time is None or end_time is None:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Shift has invalid time range")

        # Check for overlapping shifts
        overlapping_shifts = await self.shift_repo.get_shifts_by_employee_and_time(employee_id, start_time, end_time)
        if overlapping_shifts:
            return {'error': 'Overlapping shift exists'}
        # Update the existing shift's assigned_emp_id instead of creating a new shift
        if shift is not None:
            shift.assigned_emp_id = employee_id
            if status:
                shift.status = status
            await self.shift_repo.save(shift)
            return {'success': True, 'shift_id': getattr(shift, 'shift_id', None)}
        # If shift_id is None, create a new shift (legacy path)
        shift_obj = Shift(
            department_id=department_id,
            assigned_emp_id=employee_id,
            start_time=start_time,
            end_time=end_time,
            created_by_manager_id=created_by_manager_id,
            status=status or 'scheduled'
        )
        await self.shift_repo.save(shift_obj)
        return {'success': True, 'shift_id': getattr(shift_obj, 'shift_id', None)}

    # PTO CRUD
    async def create_pto(self, employee_id, start_date, end_date, reason=None):
        """
        Args:
            db: SQLAlchemy session (request-scoped, not global; managed by caller).
        """
        # employee_id should be passed explicitly as a parameter
        pto = EmployeePTO(
            pto_id=None,
            employee_id=employee_id,
            start_date=start_date,
            end_date=end_date,
            reason=reason
        )
        await self.pto_repo.save(pto)
        return {'pto_id': getattr(pto, 'pto_id', None)}

    async def update_pto(self, pto_id, **kwargs):
        """
        Args:
            db: SQLAlchemy session (request-scoped, not global; managed by caller).
        """
        await self.pto_repo.update(pto_id, **kwargs)
        return True

    async def delete_pto(self, pto_id):
        """
        Args:
            db: SQLAlchemy session (request-scoped, not global; managed by caller).
        """
        await self.pto_repo.delete(pto_id)
        return True

    async def get_pto(self, employee_id):
        """
        Args:
            db: SQLAlchemy session (request-scoped, not global; managed by caller).
        """
        employee_id = g.user['employee_id']
        return [pto.to_dict() for pto in await self.pto_repo.get_by_employee_id(employee_id)]

    # Sick Day CRUD
    async def create_sickday(self, employee_id, date, reason=None):
        """
        Args:
            db: SQLAlchemy session (request-scoped, not global; managed by caller).
        """
        employee_id = g.user['employee_id']
        sickday = EmployeeSickDay(
            sickday_id=None,
            employee_id=employee_id,
            date=date,
            reason=reason
        )
        await self.sickday_repo.save(sickday)
        return {'sickday_id': getattr(sickday, 'sickday_id', None)}

    async def update_sickday(self, sickday_id, **kwargs):
        """
        Args:
            db: SQLAlchemy session (request-scoped, not global; managed by caller).
        """
        await self.sickday_repo.update(sickday_id, **kwargs)
        return True

    async def delete_sickday(self, sickday_id):
        """
        Args:
            db: SQLAlchemy session (request-scoped, not global; managed by caller).
        """
        await self.sickday_repo.delete(sickday_id)
        return True

    async def get_sickdays(self, employee_id):
        """
        Args:
            db: SQLAlchemy session (request-scoped, not global; managed by caller).
        """
        employee_id = g.user['employee_id']
        return [sd.to_dict() for sd in await self.sickday_repo.get_by_employee_id(employee_id)]

    # Monthly schedule/traffic
    async def get_monthly_schedule(self, employee_id, year, month):
        """
        Returns all shifts for all employees in the department for the given month/year.
        PTO and sick days are NOT included.
        """
        """
        Args:
            db: SQLAlchemy session (request-scoped, not global; managed by caller).
        """
        employee_id = g.user['employee_id']
        employee = await self.employee_repo.get_by_id(employee_id)
        if not employee:
            return {'error': 'Employee not found'}
        department_id = employee.department_id
        employees = await self.employee_repo.get_all_employees(department_id=department_id)
        from datetime import datetime
        from calendar import monthrange
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month, monthrange(year, month)[1], 23, 59, 59)
        schedule = {}
        for emp in employees:
            emp_shifts = await self.shift_repo.get_shifts_by_employee_and_time(emp.emp_id, start_date, end_date)
            schedule[emp.emp_id] = {
                'shifts': emp_shifts
            }
        return schedule

    async def get_personal_monthly_schedule(self, employee_id, year, month):
        """
        Returns all shifts, PTO, and sick days for the given employee for the given month/year.
        """
        """
        Args:
            db: SQLAlchemy session (request-scoped, not global; managed by caller).
        """
        employee_id = g.user['employee_id']
        employee = await self.employee_repo.get_by_id(employee_id)
        if not employee:
            return {'error': 'Employee not found'}
        from datetime import datetime
        from calendar import monthrange
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month, monthrange(year, month)[1], 23, 59, 59)
        emp_shifts = await self.shift_repo.get_shifts_by_employee_and_time(employee_id, start_date, end_date)
        emp_pto = await self.pto_repo.get_by_employee_id(employee_id, start_date, end_date)
        emp_sick = await self.sickday_repo.get_by_employee_id(employee_id, start_date, end_date)
        return {
            'shifts': emp_shifts,
            'pto': emp_pto,
            'sickdays': emp_sick
        }
