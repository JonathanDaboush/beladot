
import DecisionFrame from '../../components/DecisionFrame';
import PageHeader from '../../components/PageHeader';
import EmptyState from '../../components/EmptyState';
import DepartmentContext from '../../components/DepartmentContext';

// This page is read-only by default. Any future mutation must use DecisionFrame modal.
const RequestsPage = () => (
  <div>
    <PageHeader
      title="Requests"
      subtitle="View your shift, PTO, and other requests"
    />
    <DepartmentContext />
    <EmptyState
      title="No requests found"
      explanation="You don’t have any requests yet. Actions will appear here once you submit or receive requests."
    />
    {/* To manage requests, use DecisionFrame modal for all mutations. */}
  </div>
);

export default RequestsPage;
