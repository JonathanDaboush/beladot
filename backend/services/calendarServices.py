"""
calendarServices.py

Service layer for calendar operations, including department and employee shift, PTO, and sick day management.
Handles calendar data retrieval for employees and managers with role-based access.
"""
# backend/service/calendarServices.py
from backend.repositories.repository.employee_repository import EmployeeRepository
from backend.repositories.repository.shift_repository import ShiftRepository
from backend.repositories.repository.employee_pto_repository import EmployeePTORepository
from backend.repositories.repository.employee_sickday_repository import EmployeeSickDayRepository

class CalendarService:
    """
    CalendarService provides methods to retrieve calendar data for departments and employees.
    Supports role-based access for managers and employees.
    """
    from sqlalchemy.ext.asyncio import AsyncSession
    def __init__(self, db: AsyncSession):
        self.db = db
        self.employee_repo = EmployeeRepository(db)
        self.shift_repo = ShiftRepository(db)
        self.pto_repo = EmployeePTORepository(db)
        self.sickday_repo = EmployeeSickDayRepository(db)

    async def get_department_calendar(self, user, year, month, view_mode="self"):
        """
        Returns department calendar data for the given month/year.
        Args:
            user: The user requesting the calendar (employee or manager)
            year: Year for the calendar
            month: Month for the calendar
            view_mode: "self" for personal view, "department" for manager view

        Returns:
            dict: Calendar data keyed by employee ID
        """
        """
        Returns department calendar data for the given month/year.
        - If view_mode == "self":
            - Employees: full details for self, limited for others (shifts: date only, no PTO/sick for others)
            - Managers: same as above, but can edit/remove all
        - If view_mode == "department" and user is manager:
            - Full details for all department employees (shifts, PTO, sick days)
        """
        from datetime import datetime
        from calendar import monthrange
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month, monthrange(year, month)[1], 23, 59, 59)
        # Get all employees in department
        employees = await self.employee_repo.get_all_employees(department_id=user.department_id)
        calendar = {}
        for emp in employees:
            emp_id = emp.emp_id
            # Shifts
            shifts = await self.shift_repo.get_shifts_by_employee_and_time(emp_id, start_date, end_date)
            # PTO
            pto = await self.pto_repo.get_by_employee_id(emp_id, start_date, end_date)
            # Sick days
            sickdays = await self.sickday_repo.get_by_employee_id(emp_id, start_date, end_date)
            if view_mode == "department" and user.role == "manager":
                calendar[emp_id] = {
                    'employee_name': emp.name,
                    'shifts': [s.to_dict() for s in shifts],
                    'pto': [p.to_dict() for p in pto],
                    'sickdays': [s.to_dict() for s in sickdays],
                }
            else:
                # view_mode == "self"
                if user.user_id == emp_id:
                    calendar[emp_id] = {
                        'employee_name': emp.name,
                        'shifts': [s.to_dict() for s in shifts],
                        'pto': [p.to_dict() for p in pto],
                        'sickdays': [s.to_dict() for s in sickdays],
                    }
                else:
                    calendar[emp_id] = {
                        'employee_name': emp.name,
                        'shifts': [{'date': s.start_time.date()} for s in shifts],
                        'pto': [],
                        'sickdays': [],
                    }
        return calendar

# Usage in controller:
# calendar = await calendarService.get_department_calendar(current_user, year, month, view_mode)
