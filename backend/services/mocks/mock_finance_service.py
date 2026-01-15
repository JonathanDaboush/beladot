from backend.services.interfaces.finance_service_interface import IFinanceService

class MockFinanceService(IFinanceService):
    async def get_issues_catalog(self):
        return []
    async def get_issue_detail(self, issue_id):
        return None
    async def create_issue(self, employee_id, description, cost, date, status):
        return None
    async def update_issue(self, issue_id, **kwargs):
        return None
    async def delete_issue(self, issue_id, confirm=False):
        return True
    async def get_reimbursements_catalog(self):
        return []
    async def get_reimbursement_detail(self, reimbursement_id):
        return None
    async def update_reimbursement(self, reimbursement_id, **kwargs):
        return None
    async def delete_reimbursement(self, reimbursement_id, confirm=False):
        return True
    async def add_reimbursement_report(self, incident_id, description, amount_approved=None, response=None):
        return None
    async def get_reimbursement(self, reimbursement_id):
        return None
    async def get_all_reimbursements(self):
        return []
    async def calculate_total_payment(self, employee_id, start_date, end_date):
        return 0.0
