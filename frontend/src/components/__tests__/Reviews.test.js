import React from 'react';
import { render, screen } from '@testing-library/react';
import Reviews from '../Reviews';

describe('Reviews', () => {
  test('renders empty state', () => {
    render(<Reviews reviews={[]} />);
    expect(screen.getByText('No reviews yet')).toBeInTheDocument();
  });

  test('renders reviews and seller response', () => {
    const reviews = [
      {
        review_id: 1,
        author_name: 'Alice',
        created_at: new Date().toISOString(),
        text: 'Great product!',
        seller_response: {
          author_name: 'Seller',
          created_at: new Date().toISOString(),
          text: 'Thanks!'
        }
      }
    ];
    render(<Reviews reviews={reviews} />);
    expect(screen.getByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('Great product!')).toBeInTheDocument();
    expect(screen.getByText(/Seller: Seller/)).toBeInTheDocument();
    expect(screen.getByText('Thanks!')).toBeInTheDocument();
  });
});
