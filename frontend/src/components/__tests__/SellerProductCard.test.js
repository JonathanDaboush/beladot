import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import SellerProductCard from '../SellerProductCard.jsx';

describe('SellerProductCard', () => {
  const product = {
    name: 'Widget',
    price: 19.99,
    category_name: 'Gadgets',
    image_url: 'http://example.com/widget.png',
  };

  test('renders product details', () => {
    render(<SellerProductCard product={product} />);
    expect(screen.getByRole('img', { name: /Widget/ })).toBeInTheDocument();
    expect(screen.getByText('Widget')).toBeInTheDocument();
    expect(screen.getByText(/Price: \$19.99/)).toBeInTheDocument();
    expect(screen.getByText(/Category: Gadgets/)).toBeInTheDocument();
  });

  test('calls onClick when clicked', async () => {
    const onClick = jest.fn();
    render(<SellerProductCard product={product} onClick={onClick} />);
    await userEvent.click(screen.getByText('Widget'));
    expect(onClick).toHaveBeenCalledTimes(1);
  });
});
