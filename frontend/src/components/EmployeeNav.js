/**
 * EmployeeNav Component
 *
 * Renders a navigation menu for employees, including general and department-specific links.
 *
 * Props:
 *   - user: The current user object, expected to have a 'department' property.
 */
import React from 'react';
import { Link } from 'react-router-dom';

// General navigation items for all employees
const generalEmployeeItems = [
  { label: 'Profile', to: '/profile' },
  { label: 'Logout', to: '/logout' }
];

// Department-specific navigation items
const departmentItems = {
  'customer_service': [
    { label: 'Refund Requests', to: '/customer_service/refund_requests' },
    { label: 'Shipment Issues', to: '/customer_service/shipment_issues' }
  ],
  'shipment': [
    { label: 'Orders', to: '/shipment/orders' },
    { label: 'Shipments', to: '/shipment/shipments' },
    { label: 'Shipment Events', to: '/shipment/shipment_events' }
  ]
};

/**
 * Main navigation component for employees.
 */
const EmployeeNav = ({ user }) => {
  const dept = user?.department;
  return (
    <nav className="employee-nav">
      <ul>
        {/* Render general navigation items */}
        {generalEmployeeItems.map(item => (
          <li key={item.to}><Link to={item.to}>{item.label}</Link></li>
        ))}
        {/* Render department-specific navigation items if available */}
        {dept && departmentItems[dept] && departmentItems[dept].map(item => (
          <li key={item.to}><Link to={item.to}>{item.label}</Link></li>
        ))}
      </ul>
    </nav>
  );
};

export default EmployeeNav;
