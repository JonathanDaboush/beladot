import React from 'react';
import { renderWithRouter } from '../../test-utils/renderWithRouter';

// Mock the wishlist hook before importing the component
jest.mock('../../hooks/useWishlistItems', () => ({
  __esModule: true,
  default: jest.fn(() => ({ data: [], loading: false, error: null }))
}));

import WishlistPage from '../WishlistPage';

describe('WishlistPage', () => {
  it('renders header and empty state when no items', () => {
    const { getByText } = renderWithRouter(<WishlistPage />);
    expect(getByText('Wishlist')).toBeInTheDocument();
    expect(getByText('No items saved')).toBeInTheDocument();
    expect(getByText('Your wishlist is empty. Add favorites to keep track of them.')).toBeInTheDocument();
  });
});
