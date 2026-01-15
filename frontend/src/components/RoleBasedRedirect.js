/**
 * RoleBasedRedirect Component
 *
 * Automatically redirects users to their appropriate portal (employee or seller)
 * based on their role after login or when visiting the root path.
 *
 * Usage:
 *   Place <RoleBasedRedirect /> at the top of your App or Layout.
 */
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

/**
 * Main redirect logic for role-based navigation.
 */
export default function RoleBasedRedirect() {
  const { isEmployee, isSeller, user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) return;
    // Only redirect from root or after login
    if (window.location.pathname === '/' || window.location.pathname === '/login') {
      if (isEmployee) {
        navigate('/employee', { replace: true });
      } else if (isSeller) {
        navigate('/seller', { replace: true });
      }
    }
  }, [isEmployee, isSeller, user, navigate]);

  // No UI rendered; this is a logic-only component
  return null;
}
