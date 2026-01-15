
import DecisionFrame from '../../components/DecisionFrame';

// This page is read-only by default. Any future mutation must use DecisionFrame modal.
const PTOPage = () => (
  <div>
    <h2>PTO</h2>
    {/* PTO request and history UI (read-only). */}
    {/* To add PTO request, use DecisionFrame modal for all mutations. */}
  </div>
);

export default PTOPage;
