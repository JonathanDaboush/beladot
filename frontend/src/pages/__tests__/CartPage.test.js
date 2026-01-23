import React from 'react';
import { renderWithRouter } from '../../test-utils/renderWithRouter';

// Apply mocks before importing the component under test
jest.mock('../../context/AuthContext', () => ({
  __esModule: true,
  useAuth: () => ({ user: { id: 1 } })
}));

jest.mock('../../api/cart', () => ({
  __esModule: true,
  fetchCartItems: jest.fn(async () => ({ items: [] })),
  editCartItemQuantity: jest.fn(),
  removeCartItem: jest.fn()
}));

// guest cart is not used in this test since user is mocked
jest.mock('../../cart/guestCart', () => ({
  getGuestCart: jest.fn(() => []),
  updateGuestCartItem: jest.fn(),
  removeGuestCartItem: jest.fn(),
  mapGuestItemsForDisplay: jest.fn(() => [])
}));

import CartPage from '../CartPage';

describe('CartPage', () => {
  it('renders header and empty state when cart is empty', async () => {
    const { findByText } = renderWithRouter(<CartPage />);
    expect(await findByText('Cart')).toBeInTheDocument();
    expect(await findByText('No items in cart')).toBeInTheDocument();
    expect(await findByText('Your cart is empty. Add items to proceed to checkout.')).toBeInTheDocument();
  });
});
