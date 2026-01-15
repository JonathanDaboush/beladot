
/**
 * useFinanceIssues
 *
 * Custom React hook to fetch and manage a list of finance issues.
 * Handles loading and error states, returns the issues data.
 *
 * Usage:
 *   const { data, loading, error } = useFinanceIssues();
 */
import { useEffect, useState } from 'react';
import { fetchIssues } from '../api/financeService';

export default function useFinanceIssues() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetchIssues()
      .then(res => {
        setData(res.items || []);
        setLoading(false);
      })
      .catch(e => {
        setError(e.toString());
        setLoading(false);
      });
  }, []);

  // Return issues data, loading, and error states
  return { data, loading, error };
}
