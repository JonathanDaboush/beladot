/**
 * AuthContext
 *
 * Provides authentication, role, and department info from the authenticated user/session object.
 * Use this context to access user state and role-based flags throughout the app.
 */
import React, { createContext, useContext, useState } from 'react';

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

  // Role and department flags derived from user/session object
  const isEmployee = user?.isEmployee === true;
  const isSeller = user?.isSeller === true;
  const isManager = user?.isManager === true;
  const department = user?.department || null;
  const job = user?.job || null;
  const managedDepartments = user?.managedDepartments || [];

  return (
    <AuthContext.Provider value={{ user, setUser, isEmployee, isSeller, isManager, department, job, managedDepartments }}>
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
