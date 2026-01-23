
import DecisionFrame from '../../components/DecisionFrame';
import PageHeader from '../../components/PageHeader';
import EmptyState from '../../components/EmptyState';
import DepartmentContext from '../../components/DepartmentContext';

// This page is read-only by default. Any future mutation must use DecisionFrame modal.
const FinancePage = () => (
  <div>
    <PageHeader title="Finance" subtitle="View your department’s finance tools and reports" />
    <DepartmentContext />
    <EmptyState
      title="No finance items"
      explanation="When finance tasks or reports are assigned, they will appear here."
      icon={"📊"}
    />
    {/* Quick links to reimbursements, payment snapshots, etc. (read-only). */}
    {/* To mutate finance data, use DecisionFrame modal for all mutations. */}
  </div>
);

export default FinancePage;
