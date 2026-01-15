// Robust global.fetch mock for all tests
beforeAll(() => {
	global.fetch = jest.fn((url) => {
		if (url === '/api/categories') {
			return Promise.resolve({
				ok: true,
				status: 200,
				json: () => Promise.resolve({ categories: [] })
			});
		}
		return Promise.resolve({
			ok: true,
			status: 200,
			json: () => Promise.resolve({})
		});
	});
});

afterAll(() => {
	if (global.fetch && global.fetch.mockClear) global.fetch.mockClear();
	delete global.fetch;
});
// Polyfill TextEncoder and TextDecoder for Jest (Node.js)
if (typeof global.TextEncoder === 'undefined') {
	global.TextEncoder = require('util').TextEncoder;
}
if (typeof global.TextDecoder === 'undefined') {
	global.TextDecoder = require('util').TextDecoder;
}
