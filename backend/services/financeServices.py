from backend.repositories.repository.reimbursement_repository import ReimbursementRepository
from backend.repositories.repository.incident_repository import IncidentRepository
from backend.repositories.repository.employee_repository import EmployeeRepository
from backend.repositories.repository.shift_repository import ShiftRepository
from backend.repositories.repository.employee_pto_repository import EmployeePTORepository
from backend.persistance.reimbursement import Reimbursement
from backend.persistance.incident import Incident
from backend.persistance.shift import Shift
from backend.persistance.employee_pto import EmployeePTO

"""
financeServices.py

Service layer for finance operations, including incident management, reimbursements, shifts, and PTO.
Provides methods for cataloging issues, retrieving details, creating, and updating incidents.
All operations are asynchronous and require a database session.
"""

from backend.services.interfaces.finance_service_interface import IFinanceService

class FinanceService(IFinanceService):
	async def calculate_total_payment(self, *args, **kwargs):
		return 0
	from sqlalchemy.ext.asyncio import AsyncSession
	def __init__(self, db: AsyncSession):
		self.db = db
		self.reimbursement_repo = ReimbursementRepository(db)
		self.incident_repo = IncidentRepository(db)
		self.employee_repo = EmployeeRepository(db)
		self.shift_repo = ShiftRepository(db)
		self.pto_repo = EmployeePTORepository(db)

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
			paid_all=False,
			deleted=False
		)
		await self.reimbursement_repo.save(reimbursement)
		return reimbursement

	async def get_reimbursement(self, reimbursement_id: int):
		"""Get a single reimbursement by ID."""
		return await self.reimbursement_repo.get_by_id(reimbursement_id)

	async def get_all_reimbursements(self):
		"""Get all reimbursements."""
		return await self.reimbursement_repo.get_all()


