import React from 'react';
import { useAuth } from '../context/AuthContext';

export default function DepartmentContext() {
  const { isEmployee, isManager, department } = useAuth();
  if (!isEmployee && !isManager) return null;
  if (!department) return null;
  const label = isManager ? `Manager • Dept ${department}` : `Department • ${department}`;
  return (
    <div className="dept-chip" aria-label="Department Context">
      {label}
    </div>
  );
}
