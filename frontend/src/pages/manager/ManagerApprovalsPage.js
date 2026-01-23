import React from 'react';
import PageHeader from '../../components/PageHeader';
import DepartmentContext from '../../components/DepartmentContext';
import EmptyState from '../../components/EmptyState';

const ManagerApprovalsPage = () => (
  <div>
    <PageHeader title="Approvals" subtitle="Review and approve department requests" />
    <DepartmentContext />
    <EmptyState
      title="No approvals pending"
      explanation="When there are items requiring approval, they will appear here."
      icon={"✅"}
    />
  </div>
);

export default ManagerApprovalsPage;
