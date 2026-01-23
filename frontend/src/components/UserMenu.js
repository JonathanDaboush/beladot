/**
 * UserMenu Component
 *
 * Displays a user menu with profile, account, order history, employee/seller options, and logout.
 * Handles menu state and options based on authentication and user role.
 *
 * Props:
 *   - onLogout: Function to call when user logs out
 */
import React, { useState } from 'react';
import './UserMenu.css';

import { useAuth } from '../context/AuthContext';

/**
 * Main user menu component.
 */
const UserMenu = ({ onLogout }) => {
  const [open, setOpen] = useState(false);
  const { user, isEmployee, isManager, isSeller, department, job } = useAuth();

  /**
   * Returns menu options based on user authentication and role.
   */
  const getMenuOptions = () => {
    if (!user) {
      return [
        { label: 'Login', action: () => window.location.href = '/login' },
        { label: 'Create Account', action: () => window.location.href = '/register' },
      ];
    }
    const options = [
      { label: 'Profile / Account', action: () => window.location.href = '/profile' },
      { label: 'Order History / Purchases', action: () => window.location.href = '/orders' },
    ];
    if (isEmployee) {
      options.push({ label: 'Employee Services', action: () => window.location.href = '/employee' });
      if (department) {
        options.push({ label: `Department: ${department}`, action: null, disabled: true });
      }
      if (job) {
        options.push({ label: `Job: ${job}`, action: null, disabled: true });
      }
    }
    if (isSeller) {
      options.push({ label: 'Seller Portal', action: () => window.location.href = '/seller' });
    }
    options.push({ label: 'Logout', action: onLogout });
    return options;
  };

  const menuOptions = getMenuOptions();

  return (
    <div className="user-menu-wrapper">
      {/* User icon toggles menu open/close */}
      <div className="user-icon" onClick={() => setOpen(!open)}>
        <span role="img" aria-label="user">👤</span>
      </div>
      {open && (
        <div className="user-dropdown">
          {/* Profile/Orders always visible for logged in users */}
          {user && (
            <>
              <div className="user-dropdown-item" onClick={() => window.location.href = '/profile'}>Profile / Account</div>
              <div className="user-dropdown-item" onClick={() => window.location.href = '/orders'}>Order History / Purchases</div>
            </>
          )}
          {/* Employee Services dropdown, for employees and managers */}
          {(isEmployee || isManager) && (
            <>
              <div className="dropdown-section-label">Employee Services</div>
              <div className="dropdown-category">
                <div className="dropdown-category-title">Schedule</div>
                <div className="user-dropdown-item" onClick={() => window.location.href = '/employee/schedule'}>Get Schedule</div>
                <div className="user-dropdown-item" onClick={() => window.location.href = '/employee/personal-schedule'}>PTO & Sick Days</div>
                <div className="user-dropdown-item" onClick={() => window.location.href = '/employee/book-shift'}>Book Shift</div>
              </div>
              <div className="dropdown-category">
                <div className="dropdown-category-title">Finance</div>
                <div className="user-dropdown-item" onClick={() => window.location.href = '/employee/reimbursement/create'}>Create Reimbursement</div>
                <div className="user-dropdown-item" onClick={() => window.location.href = '/employee/reimbursements'}>Reimbursement List</div>
                <div className="user-dropdown-item" onClick={() => window.location.href = '/employee/payment-snapshots'}>Payment Snapshots</div>
              </div>
              {department && <div className="user-dropdown-item disabled">Department: {department}</div>}
              {job && <div className="user-dropdown-item disabled">Job: {job}</div>}
            </>
          )}
          {/* Seller Portal entry, only if isSeller */}
          {isSeller && !isEmployee && (
            <div className="user-dropdown-item" onClick={() => window.location.href = '/seller'}>Seller Portal</div>
          )}
          {/* Auth links for not logged in users */}
          {!user && (
            <>
              <div className="user-dropdown-item" onClick={() => window.location.href = '/login'}>Login</div>
              <div className="user-dropdown-item" onClick={() => window.location.href = '/register'}>Create Account</div>
            </>
          )}
          {/* Logout always last if logged in */}
          {user && <div className="user-dropdown-item" onClick={onLogout}>Logout</div>}
        </div>
      )}
    </div>
  );
};

export default UserMenu;
