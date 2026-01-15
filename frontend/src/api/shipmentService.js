/**
 * Shipment Service API
 *
 * Provides functions for shipment department operations, including orders, shipments, and issues.
 * All functions interact with backend endpoints and return results or throw errors.
 */

/**
 * Fetches all orders.
 * @returns {Promise<Array>} List of orders
 */
export async function getOrders() {
  const res = await fetch('/api/get_orders', { method: 'POST' });
  const data = await res.json();
  return data.result || [];
}

/**
 * Fetches details for a specific order.
 * @param {string|number} orderId
 * @returns {Promise<object>} Order detail
 */
export async function getOrderDetails(orderId) {
  const res = await fetch('/api/get_order_details', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ order_id: orderId })
  });
  const data = await res.json();
  return data.result;
}

/**
 * Creates a shipment event for an order.
 * @param {string|number} orderId
 * @param {object} eventData
 */
export async function createShipmentEvent(orderId, eventData) {
  await fetch('/api/create_shipment_event', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ order_id: orderId, ...eventData })
  });
}

/**
 * Fetches all shipments.
 * @returns {Promise<Array>} List of shipments
 */
export async function getShipments() {
  const res = await fetch('/api/get_shipments', { method: 'POST' });
  const data = await res.json();
  return data.result || [];
}

/**
 * Fetches a specific shipment by ID.
 * @param {string|number} shipmentId
 * @returns {Promise<object>} Shipment detail
 */
export async function getShipment(shipmentId) {
  const res = await fetch('/api/get_shipment', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ shipment_id: shipmentId })
  });
  const data = await res.json();
  return data.result;
}

/**
 * Fetches details for a specific shipment.
 * @param {string|number} shipmentId
 * @returns {Promise<object>} Shipment detail
 */
export async function getShipmentDetails(shipmentId) {
  const res = await fetch('/api/get_shipment_details', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ shipment_id: shipmentId })
  });
  const data = await res.json();
  return data.result;
}

/**
 * Edits a shipment issue by ID and fields.
 * @param {string|number} issueId
 * @param {object} fields
 */
export async function editShipmentIssue(issueId, fields) {
  await fetch('/api/edit_shipment_issue', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ issue_id: issueId, ...fields })
  });
}

export async function deleteShipmentIssue(issueId) {
  await fetch('/api/delete_shipment_issue', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ issue_id: issueId })
  });
}

export async function getShipmentEvents() {
  const res = await fetch('/api/get_shipment_events', { method: 'POST' });
  const data = await res.json();
  return data.result || [];
}

export async function getShipmentEvent(eventId) {
  const res = await fetch('/api/get_shipment_event', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ event_id: eventId })
  });
  const data = await res.json();
  return data.result;
}
