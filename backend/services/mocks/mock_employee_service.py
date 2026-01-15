from backend.services.interfaces.employee_service_interface import IEmployeeService

class MockEmployeeService(IEmployeeService):
    async def get_reimbursement_details(self, reimbursement_id):
        return None
    async def create_reimbursement_claim(self, incident_id, description, amount_requested=None, paystub_url=None):
        return None
    async def book_shift(self, employee_id, shift_id=None, start_time=None, end_time=None, department_id=None, created_by_manager_id=None, status=None):
        return {'success': True, 'shift': None}
    async def create_pto(self, employee_id, start_date, end_date, reason=None):
        return None
    async def update_pto(self, pto_id, **kwargs):
        return None
    async def delete_pto(self, pto_id):
        return True
    async def get_pto(self, employee_id):
        return []
    async def create_sickday(self, employee_id, date, reason=None):
        return None
    async def update_sickday(self, sickday_id, **kwargs):
        return None
    async def delete_sickday(self, sickday_id):
        return True
    async def get_sickdays(self, employee_id):
        return []
    async def get_monthly_schedule(self, employee_id, year, month):
        return {}
    async def get_personal_monthly_schedule(self, employee_id, year, month):
        return {}
