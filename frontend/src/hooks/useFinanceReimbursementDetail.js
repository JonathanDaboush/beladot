
/**
 * useFinanceReimbursementDetail
 *
 * Custom React hook to fetch and manage details for a single finance reimbursement.
 * Handles loading and error states, returns the reimbursement detail data.
 *
 * @param {string|number} id - The ID of the reimbursement to fetch.
 * @returns {object} { data, loading, error }
 */
import { useEffect, useState } from 'react';
import { fetchReimbursementDetail } from '../api/financeService';

export default function useFinanceReimbursementDetail(id) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    fetchReimbursementDetail(id)
      .then(res => {
        setData(res.item || null);
        setLoading(false);
      })
      .catch(e => {
        setError(e.toString());
        setLoading(false);
      });
  }, [id]);

  // Return reimbursement detail data, loading, and error states
  return { data, loading, error };
}
