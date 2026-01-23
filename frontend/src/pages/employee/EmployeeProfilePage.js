
import DecisionFrame from '../../components/DecisionFrame';
import PageHeader from '../../components/PageHeader';
import DepartmentContext from '../../components/DepartmentContext';
import EmptyState from '../../components/EmptyState';

// This page is read-only by default. Any future mutation must use DecisionFrame modal.
const EmployeeProfilePage = () => (
  <div>
    <PageHeader
      title="Employee Profile"
      subtitle="Your personal information and employment details"
    />
    <DepartmentContext />
    <EmptyState
      title="Profile"
      explanation="Profile details will appear here. Editing requires approval and will use the DecisionFrame modal."
    />
    {/* To edit profile, use DecisionFrame modal for all mutations. */}
  </div>
);

export default EmployeeProfilePage;
