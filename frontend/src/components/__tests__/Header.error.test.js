import React from 'react';
import { screen, waitFor } from '@testing-library/react';
import Header from '../Header';
import { renderWithRouter } from '../../test-utils/renderWithRouter';

jest.mock('../../context/AuthContext', () => ({
  useAuth: () => ({ activeRole: 'user', availableRoles: ['user'] }),
}));

jest.mock('../../hooks/usePortalType', () => ({
  usePortalType: () => 'user',
}));

describe('Header (error path)', () => {
  afterEach(() => {
    jest.resetAllMocks();
  });

  it('renders header without relying on categories API', async () => {
    global.fetch = jest.fn(() => Promise.resolve({ json: () => Promise.resolve({}) }));
    renderWithRouter(<Header />);
    await waitFor(() => expect(screen.getByText(/Bela/i)).toBeInTheDocument());
    // Nav still renders role-scoped items
    await waitFor(() => expect(screen.getByText('Browse / Catalog')).toBeInTheDocument());
  });
});
