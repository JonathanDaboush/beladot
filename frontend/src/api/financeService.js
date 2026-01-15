/**
 * Finance API service
 *
 * Provides functions to fetch finance issues and reimbursements from the backend API.
 * Each function throws an error if the request fails.
 */

/**
 * Fetches all finance issues.
 * @returns {Promise<object>} Issues data
 */
export async function fetchIssues() {
  const res = await fetch('/api/finance/issues');
  if (!res.ok) throw new Error('Failed to fetch issues');
  return res.json();
}

/**
 * Fetches details for a specific finance issue.
 * @param {string|number} id - Issue ID
 * @returns {Promise<object>} Issue detail data
 */
export async function fetchIssueDetail(id) {
  const res = await fetch(`/api/finance/issues/${id}`);
  if (!res.ok) throw new Error('Failed to fetch issue detail');
  return res.json();
}

/**
 * Fetches all finance reimbursements.
 * @returns {Promise<object>} Reimbursements data
 */
export async function fetchReimbursements() {
  const res = await fetch('/api/finance/reimbursements');
  if (!res.ok) throw new Error('Failed to fetch reimbursements');
  return res.json();
}

/**
 * Fetches details for a specific finance reimbursement.
 * @param {string|number} id - Reimbursement ID
 * @returns {Promise<object>} Reimbursement detail data
 */
export async function fetchReimbursementDetail(id) {
  const res = await fetch(`/api/finance/reimbursements/${id}`);
  if (!res.ok) throw new Error('Failed to fetch reimbursement detail');
  return res.json();
}
