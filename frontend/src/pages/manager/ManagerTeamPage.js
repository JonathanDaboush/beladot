import React from 'react';
import PageHeader from '../../components/PageHeader';
import DepartmentContext from '../../components/DepartmentContext';
import EmptyState from '../../components/EmptyState';

const ManagerTeamPage = () => (
  <div>
    <PageHeader title="Team / Employees" subtitle="View and manage your team" />
    <DepartmentContext />
    <EmptyState
      title="No team data"
      explanation="Team members and assignments will appear here when available."
      icon={"👥"}
    />
  </div>
);

export default ManagerTeamPage;
