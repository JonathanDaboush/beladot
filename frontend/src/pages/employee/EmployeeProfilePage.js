
import DecisionFrame from '../../components/DecisionFrame';

// This page is read-only by default. Any future mutation must use DecisionFrame modal.
const EmployeeProfilePage = () => (
  <div>
    <h2>Employee Profile</h2>
    {/* Employee-specific profile info and edit UI (read-only). */}
    {/* To edit profile, use DecisionFrame modal for all mutations. */}
  </div>
);

export default EmployeeProfilePage;
