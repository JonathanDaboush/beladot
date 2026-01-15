import React, { memo } from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import './EmployeeServicesLayout.css';
import { useAuth } from '../../context/AuthContext';
import DecisionFrame from '../../components/DecisionFrame';

/**
 * Memoized subcomponent to render a list of navigation links for the sidebar.
 * Props:
 *  - options: Array of navigation objects with { label, to }
 */
const NavOptionsList = memo(({ options }) => (
  <>
    {options.map(opt => (
      <li key={opt.to}>
        <NavLink
          to={opt.to}
          className={({ isActive }) => (isActive ? 'active' : '')}
          end
        >
          {opt.label}
        </NavLink>
      </li>
    ))}
  </>
));

/**
 * Navigation options for the employee portal sidebar
 */
const navOptions = [
  { label: 'Home', to: '/employee' },
  { label: 'Schedule', to: '/employee/schedule' },
  { label: 'Finance', to: '/employee/finance' },
  { label: 'Requests', to: '/employee/requests' },
  { label: 'PTO', to: '/employee/pto' },
  { label: 'Incidents', to: '/employee/incidents' },
  { label: 'Profile', to: '/employee/profile' },
];

/**
 * EmployeeServicesLayout
 * ---------------------
 * Main layout for the employee portal.
 * Renders sidebar navigation and main content area.
 * Checks authorization using AuthContext.
 */
const EmployeeServicesLayout = () => {
  const { department, job, isEmployee, isManager } = useAuth();

  if (!(isEmployee || isManager)) {
    // If the user is not authorized, show a clear message
    return <div style={{ padding: '2rem', color: '#b91c1c' }}>Not authorized.</div>;
  }

  return (
    <div className="employee-layout">
      <aside className="employee-sidebar">
        <nav>
          <ul>
            {/* Render the sidebar navigation using a memoized subcomponent */}
            <NavOptionsList options={navOptions} />
          </ul>
        </nav>
        {department && <div className="sidebar-info">Dept: {department}</div>}
        {job && <div className="sidebar-info">Job: {job}</div>}
      </aside>

      <main className="employee-main">
        <Outlet />
        {/* To mutate layout, use DecisionFrame modal for all mutations */}
      </main>
    </div>
  );
};

export default EmployeeServicesLayout;
