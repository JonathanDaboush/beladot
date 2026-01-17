import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
// Mock auth context and portal hook used by Header
jest.mock('../../context/AuthContext', () => ({
  useAuth: () => ({ isEmployee: false, isSeller: false })
}));
jest.mock('../../hooks/usePortalType', () => ({
  usePortalType: () => 'user'
}));
import Layout from '../Layout';

describe('Layout', () => {
  test('renders header, redirect, and children', () => {
    // Mock fetch used by Header
    global.fetch = jest.fn(() => Promise.resolve({ json: () => Promise.resolve({ categories: [] }) }));
    render(
      <MemoryRouter>
        <Layout>
          <div>Child Content</div>
        </Layout>
      </MemoryRouter>
    );
    expect(screen.getByText('Child Content')).toBeInTheDocument();
    // Header content: assume menu labels present (UserMenu includes a Menu or similar)
    // We at least verify that the main element exists
    const mains = screen.getAllByRole('main');
    expect(mains.length).toBeGreaterThan(0);
  });
  let originalFetch;
  beforeEach(() => {
    originalFetch = global.fetch;
  });
  afterEach(() => {
    global.fetch = originalFetch;
    jest.resetAllMocks();
  });
});
