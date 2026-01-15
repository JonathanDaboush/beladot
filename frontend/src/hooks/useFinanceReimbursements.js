
/**
 * useFinanceReimbursements
 *
 * Custom React hook to fetch and manage a list of finance reimbursements.
 * Handles loading and error states, returns the reimbursements data.
 *
 * Usage:
 *   const { data, loading, error } = useFinanceReimbursements();
 */
import { useEffect, useState } from 'react';
import { fetchReimbursements } from '../api/financeService';

export default function useFinanceReimbursements() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetchReimbursements()
      .then(res => {
        setData(res.items || []);
        setLoading(false);
      })
      .catch(e => {
        setError(e.toString());
        setLoading(false);
      });
  }, []);

  // Return reimbursements data, loading, and error states
  return { data, loading, error };
}
