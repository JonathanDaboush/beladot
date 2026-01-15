/**
 * Customer Service API
 *
 * Provides functions for customer refund requests and shipment grievance reports.
 * All functions interact with backend endpoints and return results or throw errors.
 */

/**
 * Fetches all customer refund requests.
 * @returns {Promise<Array>} List of refund requests
 */
export async function getAllCustomerRefundRequests() {
  const res = await fetch('/api/get_all_customer_refund_requests', { method: 'POST' });
  const data = await res.json();
  return data.result || [];
}

/**
 * Fetches a specific refund request by ID.
 * @param {string|number} refundRequestId
 * @returns {Promise<object>} Refund request detail
 */
export async function getSpecificRefundRequest(refundRequestId) {
  const res = await fetch('/api/get_specific_refund_request', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refund_request_id: refundRequestId })
  });
  const data = await res.json();
  return data.result;
}

/**
 * Approves or denies a refund request.
 * @param {string|number} refundRequestId
 * @param {string} action - 'approve' or 'deny'
 * @param {number} refundAmount
 * @param {string} description
 */
export async function approveOrDenyRefund(refundRequestId, action, refundAmount, description) {
  const status = action === 'approve' ? 'approved' : 'denied';
  await fetch('/api/process_customer_complaint', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refund_request_id: refundRequestId, status, refund_amount: refundAmount, description })
  });
  // Optionally refetch or handle result
}

/**
 * Fetches all shipment grievance reports.
 * @returns {Promise<Array>} List of grievance reports
 */
export async function getShipmentGrievanceReports() {
  const res = await fetch('/api/get_shipment_greivence_reports', { method: 'POST' });
  const data = await res.json();
  return data.result || [];
}

/**
 * Fetches details for a specific grievance report.
 * @param {string|number} issueId
 * @returns {Promise<object>} Grievance detail
 */
export async function getGrievanceDetails(issueId) {
  const res = await fetch('/api/get_greivence_details', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ issue_id: issueId })
  });
  const data = await res.json();
  return data.result;
}

/**
 * Processes a shipment report with a given fault type.
 * @param {string|number} issueId
 * @param {string} faultType
 */
export async function processShipmentReport(issueId, faultType) {
  await fetch('/api/process_shipment_report', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ issue_id: issueId, issue_type: faultType })
  });
}
