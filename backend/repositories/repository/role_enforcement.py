"""
role_enforcement.py

Role-based access control utilities for API endpoints.
Includes decorators for enforcing manager department restrictions.
FastAPI-compatible implementation.
"""

from functools import wraps
from fastapi import Request
from fastapi.responses import JSONResponse

async def get_employee_department(employee_repo, employee_id):
    """
    Retrieve the department ID for a given employee.
    Args:
        employee_repo: Repository for employee data.
        employee_id: ID of the employee.
    Returns:
        int or None: Department ID if found, else None.
    """
    employee = await employee_repo.get_by_id(employee_id)
    if not employee:
        return None
    return getattr(employee, 'department_id', None)

def manager_department_required(employee_repo):
    """
    Decorator for endpoints: Only allow managers to act on employees in their own department.
    Assumes request.state.identity is set with 'role', 'user_id', and 'department_id'.
    Args:
        employee_repo: Repository for employee data.
    Returns:
        function: Decorator for endpoint function.
    """
    def decorator(f):
        @wraps(f)
        async def wrapper(request: Request, *args, **kwargs):
            identity = getattr(request.state, 'identity', None)
            if not identity:
                return JSONResponse({'error': 'Unauthorized'}, status_code=401)
            if identity.get('role') != 'manager':
                return JSONResponse({'error': 'Forbidden'}, status_code=403)

            data = None
            try:
                data = await request.json()
            except Exception:
                # Fallback to explicit dict passed in kwargs
                data = kwargs.get('data')
            employee_id = (data.get('employee_id') if isinstance(data, dict) else None) or kwargs.get('employee_id')
            if not employee_id:
                return JSONResponse({'error': 'employee_id required'}, status_code=400)

            emp_dept = await get_employee_department(employee_repo, employee_id)
            if emp_dept != identity.get('department_id'):
                return JSONResponse({'error': 'Forbidden'}, status_code=403)

            return await f(request, *args, **kwargs)
        return wrapper
    return decorator

# Usage in app.py:
# from backend.repositories.repository.role_enforcement import manager_department_required
# @app.route('/api/create_pto', methods=['POST'])
# @manager_department_required(employeeServices.employee_repo)
# async def ctrl_create_pto():
#     ...
