import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';

jest.mock('../../context/AuthContext', () => ({
  useAuth: () => ({ user: null, isEmployee: false, isManager: false, isSeller: false }),
}));
// Also mock the path as imported by UserMenu (../context/AuthContext)

import UserMenu from '../UserMenu';

test('shows login options when not authenticated', () => {
  const onLogout = jest.fn();
  render(<UserMenu onLogout={onLogout} />);
  fireEvent.click(screen.getByRole('img', { name: /user/i }));
  expect(screen.getByText(/Login/i)).toBeInTheDocument();
  expect(screen.getByText(/Create Account/i)).toBeInTheDocument();
});
