from backend.repository.reimbursement_repository import ReimbursementRepository
from backend.repository.incident_repository import IncidentRepository
from backend.repository.employee_repository import EmployeeRepository
from backend.repository.shift_repository import ShiftRepository
from backend.repository.employee_pto_repository import EmployeePTORepository
from backend.model.reimbursement import Reimbursement
from backend.persistance.incident import Incident
from backend.model.shift import Shift
from backend.model.employee_pto import EmployeePTO

"""
financeServices.py

Service layer for finance operations, including incident management, reimbursements, shifts, and PTO.
Provides methods for cataloging issues, retrieving details, creating, and updating incidents.
All operations are asynchronous and require a database session.
"""

from backend.services.interfaces.finance_service_interface import IFinanceService

class FinanceService(IFinanceService):
	def __init__(self, db):
		self.db = db
		self.incident_repo = IncidentRepository(db)
		self.employee_repo = EmployeeRepository(db)
		# ... other repos as needed

	async def get_issues_catalog(self):
		issues = await self.incident_repo.get_all()
		result = []
		for issue in issues:
			if issue.deleted:
				continue
			employee = await self.employee_repo.get_by_id(issue.employee_id) if hasattr(issue, 'employee_id') else None
			result.append({
				'employee_name': getattr(employee, 'name', None) if employee else None,
				'date': issue.date,
				'status': issue.status,
				'issue_id': issue.incident_id
			})
		return result

	async def get_issue_detail(self, issue_id):
		issue = await self.incident_repo.get_by_id(issue_id)
		if not issue or issue.deleted:
			return None
		employee = await self.employee_repo.get_by_id(issue.employee_id) if hasattr(issue, 'employee_id') else None
		return {
			'description': issue.description,
			'cost': issue.cost,
			'date': issue.date,
			'status': issue.status,
			'employee': {
				'name': getattr(employee, 'name', None),
				'dob': getattr(employee, 'dob', None),
				'phone': getattr(employee, 'phone', None),
				'email': getattr(employee, 'email', None),
				'image': getattr(employee, 'image', None)
			} if employee else None
		}

	async def create_issue(self, employee_id, description, cost, date, status):
		issue = Incident(
			employee_id=employee_id,
			description=description,
			cost=cost,
			date=date,
			status=status,
			deleted=False
		)
		await self.incident_repo.save(issue)
		return {'issue_id': issue.incident_id}

	async def update_issue(self, issue_id, **kwargs):
		issue = await self.incident_repo.get_by_id(issue_id)
		if not issue or issue.deleted:
			return None
		if str(issue.status).lower() in ['approved', 'settled', 'finance_approved']:
			return None
		await self.incident_repo.update(issue_id, **kwargs)
		return True

	async def delete_issue(self, issue_id, confirm=False):
		if not confirm:
			return False
		await self.incident_repo.delete(issue_id)
		return True

	async def can_create_reimbursement(self, issue_id):
		issue = await self.incident_repo.get_by_id(issue_id)
		return issue is not None and not issue.deleted

	async def get_reimbursements_catalog(self):
		reimbursements = await self.reimbursement_repo.get_all()
		result = []
		for r in reimbursements:
			if r.deleted:
				continue
			issue = await self.incident_repo.get_by_id(r.incident_id) if hasattr(r, 'incident_id') else None
			employee = await self.employee_repo.get_by_id(issue.employee_id) if issue and hasattr(issue, 'employee_id') else None
			result.append({
				'employee_name': getattr(employee, 'name', None) if employee else None,
				'status': r.status,
				'date': issue.date if issue else None,
				'reimbursement_id': r.reimbursement_id
			})
		return result

	async def get_reimbursement_detail(self, reimbursement_id):
		r = await self.reimbursement_repo.get_by_id(reimbursement_id)
		if not r or r.deleted:
			return None
		issue = await self.incident_repo.get_by_id(r.incident_id) if hasattr(r, 'incident_id') else None
		employee = await self.employee_repo.get_by_id(issue.employee_id) if issue and hasattr(issue, 'employee_id') else None
		return {
			'amount': r.amount_approved,
			'status': r.status,
			'date': getattr(r, 'created', None),
			'description': r.description,
			'issue': {
				'description': issue.description if issue else None,
				'cost': issue.cost if issue else None,
				'date': issue.date if issue else None,
				'status': issue.status if issue else None
			} if issue else None,
			'employee': {
				'name': getattr(employee, 'name', None),
				'dob': getattr(employee, 'dob', None),
				'phone': getattr(employee, 'phone', None),
				'email': getattr(employee, 'email', None),
				'image': getattr(employee, 'image', None)
			} if employee else None
		}

	async def update_reimbursement(self, reimbursement_id, **kwargs):
		r = await self.reimbursement_repo.get_by_id(reimbursement_id)
		if not r or r.deleted:
			return None
		if str(r.status).lower() in ['approved', 'settled', 'finance_approved']:
			return None
		await self.reimbursement_repo.update(reimbursement_id, **kwargs)
		return True
	# Authority Levels (documented for reviewers)
	# Action                Customer Service   Shipment   Finance
	# Create issue          Yes                Yes        No
	# View issue            Yes                Yes        Yes
	# Edit incident facts   Limited            Limited    No
	# Create reimbursement  No                 No         Yes
	# Approve reimbursement No                 No         Yes
	# Finalize/settle       No                 No         Yes

	# Cross-department state signaling
	# Use IncidentStatus.AWAITING_FINANCE_REVIEW and ReimbursementStatus.AWAITING_FINANCE_REVIEW

	async def delete_reimbursement(self, reimbursement_id, confirm=False):
		if not confirm:
			return False
		await self.reimbursement_repo.delete(reimbursement_id)
		return True

	async def add_reimbursement_report(self, incident_id, description, amount_approved=None, response=None):
		"""
		Add a new reimbursement report with status_addressed set to False by default.
		"""
		reimbursement = Reimbursement(
			reimbursement_id=None,
			incident_id=incident_id,
			description=description,
			response=response,
			amount_approved=amount_approved,
			status=False,
			status_addressed=False,
			paid_all=False
		)
		await self.reimbursement_repo.save(reimbursement)
		return reimbursement

	# Reimbursement CRUD
	async def get_reimbursement(self, reimbursement_id):
		return await self.reimbursement_repo.get_by_id(reimbursement_id)

	async def get_all_reimbursements(self):
		return await self.reimbursement_repo.get_all()

	async def update_reimbursement(self, reimbursement_id, **kwargs):
		return await self.reimbursement_repo.update(reimbursement_id, **kwargs)

	async def delete_reimbursement(self, reimbursement_id):
		return await self.reimbursement_repo.delete(reimbursement_id)
	def __init__(self, db):
		self.db = db
		self.reimbursement_repo = ReimbursementRepository(db)
		self.incident_repo = IncidentRepository(db)
		self.employee_repo = EmployeeRepository(db)
		self.shift_repo = ShiftRepository(db)
		self.pto_repo = EmployeePTORepository(db)

	async def calculate_total_payment(self, employee_id, start_date, end_date):
		employee = await self.employee_repo.get_by_id(employee_id)
		if not employee:
			return 0.0
		hourly_rate = getattr(employee, 'hourly_rate', 0.0)
		# Calculate total hours worked
		shifts = await self.shift_repo.get_shifts_by_employee_and_time(employee_id, start_date, end_date)
		total_hours = sum([(s.end_time - s.start_time).total_seconds() / 3600 for s in shifts])
		# Calculate PTO hours
		pto_list = await self.pto_repo.get_by_employee_id(employee_id, start_date, end_date)
		pto_hours = 0.0
		for pto in pto_list:
			pto_start = max(pto.start_date, start_date)
			pto_end = min(pto.end_date, end_date)
			pto_hours += (pto_end - pto_start).total_seconds() / 3600
		# Bonuses within timeframe
		bonuses = 0.0
		if hasattr(employee, 'bonuses') and isinstance(employee.bonuses, list):
			for bonus in employee.bonuses:
				if hasattr(bonus, 'date') and hasattr(bonus, 'amount'):
					if start_date <= bonus.date <= end_date:
						bonuses += bonus.amount
		elif hasattr(employee, 'bonuses'):
			bonuses = getattr(employee, 'bonuses', 0.0)
		# Subtract unpaid incident costs (all unresolved incidents up to end_date)
		incidents = await self.incident_repo.get_unresolved_incidents(end_date)
		# Address incidents before calculation
		for i in incidents:
			if hasattr(i, 'addressed') and not i.addressed:
				i.addressed = True
				await self.incident_repo.update(i.incident_id, addressed=True)
		unpaid_incident_costs = sum([i.cost for i in incidents if hasattr(i, 'date') and i.date <= end_date])
		# Add reimbursements (only those marked addressed/approved)
		reimbursements = await self.reimbursement_repo.get_by_employee_id(employee_id)
		# Address reimbursements before calculation
		for r in reimbursements:
			if hasattr(r, 'status_addressed') and not r.status_addressed:
				r.status_addressed = True
				await self.reimbursement_repo.update(r.reimbursement_id, status_addressed=True)
		reimbursements_total = sum([r.amount_approved or 0.0 for r in reimbursements if r.status_addressed])
		# Ensure any unpaid past reimbursements or incidents are included
		past_unpaid_reimbursements = sum([
			(r.amount_approved or 0.0) for r in reimbursements if not r.status_addressed and not getattr(r, 'paid_all', False)
		])
		net_total = total_hours * hourly_rate + pto_hours * hourly_rate + bonuses + reimbursements_total - unpaid_incident_costs - past_unpaid_reimbursements
		return net_total
 

	