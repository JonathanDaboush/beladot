
/**
 * usePortalType
 *
 * Custom React hook to determine the portal type based on the current route.
 * Returns 'employee', 'seller', or 'user' depending on the pathname.
 *
 * Usage:
 *   const portalType = usePortalType();
 */
import { useLocation } from 'react-router-dom';

export function usePortalType() {
  const location = useLocation();
  // Determine portal type by route prefix
  if (location.pathname.startsWith('/employee')) return 'employee';
  if (location.pathname.startsWith('/seller')) return 'seller';
  return 'user';
}
