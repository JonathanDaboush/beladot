
import DecisionFrame from '../../components/DecisionFrame';

// This page is read-only by default. Any future mutation must use DecisionFrame modal.
const FinancePage = () => (
  <div>
    <h2>Finance Overview</h2>
    {/* Quick links to reimbursements, payment snapshots, etc. (read-only). */}
    {/* To mutate finance data, use DecisionFrame modal for all mutations. */}
  </div>
);

export default FinancePage;
