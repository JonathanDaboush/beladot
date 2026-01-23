import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

/**
 * Mock AuthContext
 */
jest.mock('./context/AuthContext', () => ({
  useAuth: () => ({
    user: null,
    activeRole: 'user',
    availableRoles: ['user'],
    login: jest.fn(),
    logout: jest.fn(),
  }),
}));

/**
 * Stable fetch mock
 * MUST be beforeEach, not beforeAll
 */
beforeEach(() => {
  global.fetch = jest.fn((url) =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () =>
        Promise.resolve(
          url === '/api/categories'
            ? { categories: [] }
            : {}
        ),
    })
  );
});

/**
 * Clean teardown to avoid leaked handles
 */
afterEach(() => {
  jest.restoreAllMocks();
});

/**
 * Test
 */
test('renders homepage welcome', async () => {
  render(<App />);
  const heading = await screen.findByText(/Welcome to Bela/i);
  expect(heading).toBeInTheDocument();
});
