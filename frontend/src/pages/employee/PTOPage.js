
import DecisionFrame from '../../components/DecisionFrame';
import PageHeader from '../../components/PageHeader';
import EmptyState from '../../components/EmptyState';
import DepartmentContext from '../../components/DepartmentContext';

// This page is read-only by default. Any future mutation must use DecisionFrame modal.
const PTOPage = () => (
  <div>
    <PageHeader
      title="PTO"
      subtitle="View your PTO requests and history"
    />
    <DepartmentContext />
    <EmptyState
      title="No PTO requests"
      explanation="You don’t have any PTO requests yet. Submit requests via the PTO form when available."
    />
    {/* To add PTO request, use DecisionFrame modal for all mutations. */}
  </div>
);

export default PTOPage;
