
/**
 * useFinanceIssueDetail
 *
 * Custom React hook to fetch and manage details for a single finance issue.
 * Handles loading and error states, returns the issue detail data.
 *
 * @param {string|number} id - The ID of the finance issue to fetch.
 * @returns {object} { data, loading, error }
 */
import { useEffect, useState } from 'react';
import { fetchIssueDetail } from '../api/financeService';

export default function useFinanceIssueDetail(id) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    fetchIssueDetail(id)
      .then(res => {
        setData(res.item || null);
        setLoading(false);
      })
      .catch(e => {
        setError(e.toString());
        setLoading(false);
      });
  }, [id]);

  // Return issue detail data, loading, and error states
  return { data, loading, error };
}
