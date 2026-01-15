// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';

import fetchMock from 'jest-fetch-mock';
fetchMock.enableMocks();


beforeAll(() => {
	global.fetch = jest.fn((url, options) => {
		// Default mock for all API endpoints
		let response = { ok: true, status: 200, json: () => Promise.resolve({}) };
		if (url === '/api/categories') {
			response = { ok: true, status: 200, json: () => Promise.resolve({ categories: [] }) };
		} else if (url === '/api/cart') {
			response = { ok: true, status: 200, json: () => Promise.resolve([]) };
		} else if (url === '/api/wishlist') {
			response = { ok: true, status: 200, json: () => Promise.resolve([]) };
		} else if (url === '/api/get_all_customer_refund_requests') {
			response = { ok: true, status: 200, json: () => Promise.resolve({ result: [] }) };
		} else if (url === '/api/get_orders') {
			response = { ok: true, status: 200, json: () => Promise.resolve({ result: [] }) };
		} else if (url === '/api/get_shipments') {
			response = { ok: true, status: 200, json: () => Promise.resolve({ result: [] }) };
		} else if (url.startsWith('/api/get_shipment_greivence_reports')) {
			response = { ok: true, status: 200, json: () => Promise.resolve({ result: [] }) };
		} else if (url.startsWith('/api/finance/issues')) {
			response = { ok: true, status: 200, json: () => Promise.resolve({ result: [] }) };
		} else if (url.startsWith('/api/finance/reimbursements')) {
			response = { ok: true, status: 200, json: () => Promise.resolve({ result: [] }) };
		}
		return Promise.resolve(response);
	});
});
