import React from 'react';
import PageHeader from '../../components/PageHeader';
import DepartmentContext from '../../components/DepartmentContext';
import EmptyState from '../../components/EmptyState';

const ManagerDepartmentOverviewPage = () => (
  <div>
    <PageHeader title="Department Overview" subtitle="Overview of schedules, incidents, and performance" />
    <DepartmentContext />
    <EmptyState
      title="No department data"
      explanation="Department metrics and reports will appear here when available."
      icon={"🏢"}
    />
  </div>
);

export default ManagerDepartmentOverviewPage;
