/**
 * AuthContext
 *
 * Provides authentication, role, and department info from the authenticated user/session object.
 * Use this context to access user state and role-based flags throughout the app.
 */
import React, { createContext, useContext, useMemo, useState } from 'react';

const AuthContext = createContext();

/**
 * AuthProvider
 *
 * Wraps the app and provides authentication state and role info.
 * Replace the user state logic with real session/user fetch logic in production.
 */
export const AuthProvider = ({ children }) => {
  // Example: Replace with real session/user fetch logic
  const [user, setUser] = useState(null); // Should be set after login

  // Determine available roles from user/session
  const availableRoles = useMemo(() => {
    const roles = ['user'];
    if (user?.isEmployee) roles.push('employee');
    if (user?.isSeller) roles.push('seller');
    if (user?.isManager) roles.push('manager');
    return roles;
  }, [user]);

  // Active role controls UI; default to 'user' when not logged in
  const [activeRole, setActiveRole] = useState('user');

  // Keep department/job context for employee/manager views
  const isEmployee = availableRoles.includes('employee');
  const isSeller = availableRoles.includes('seller');
  const isManager = availableRoles.includes('manager');
  const department = user?.department || null;
  const job = user?.job || null;
  const managedDepartments = user?.managedDepartments || [];

  const value = {
    user,
    setUser,
    availableRoles,
    activeRole,
    setActiveRole,
    isEmployee,
    isSeller,
    isManager,
    department,
    job,
    managedDepartments,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

/**
 * useAuth
 *
 * Custom hook to access authentication and role info from AuthContext.
 */
export const useAuth = () => useContext(AuthContext);
