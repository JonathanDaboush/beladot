
import DecisionFrame from '../../components/DecisionFrame';
import PageHeader from '../../components/PageHeader';
import EmptyState from '../../components/EmptyState';
import DepartmentContext from '../../components/DepartmentContext';

// This page is read-only by default. Any future mutation must use DecisionFrame modal.
const IncidentsPage = () => (
  <div>
    <PageHeader title="Incidents" subtitle="View and report workplace incidents" />
    <DepartmentContext />
    <EmptyState
      title="No incidents reported"
      explanation="Reported incidents will appear here."
      icon={"⚠️"}
    />
    {/* To report an incident, use DecisionFrame modal for all mutations. */}
  </div>
);

export default IncidentsPage;
