import React from 'react';
import { render, screen } from '@testing-library/react';
import ProductList from '../ProductList';
import Reviews from '../Reviews';
import SellerProductCard from '../SellerProductCard.jsx';
import { fireEvent } from '@testing-library/react';

// Stub CSS import used by SellerProductCard for Jest
jest.mock('src/components/SellerProductCard.css', () => ({}), { virtual: true });

describe('ProductList', () => {
  it('renders empty state when no products', () => {
    render(<ProductList products={[]} />);
    expect(screen.getByText(/No products available/i)).toBeInTheDocument();
  });

  it('renders product cards from props', () => {
    const products = [
      {
        product_id: 1,
        image_url: '/img/1.png',
        name: 'Alpha',
        price: 10,
        category_name: 'Cat A',
        subcategory_name: 'Sub A',
        rating: 4.5,
      },
      {
        product_id: 2,
        image_url: '/img/2.png',
        name: 'Beta',
        price: 20,
        category_name: 'Cat B',
        subcategory_name: 'Sub B',
        rating: 3.9,
      },
    ];

    render(<ProductList products={products} />);
    expect(screen.getByText('Alpha')).toBeInTheDocument();
    expect(screen.getByText('Beta')).toBeInTheDocument();
    expect(screen.getAllByRole('img').length).toBe(2);
  });

  it('Reviews shows empty state and list with seller response', () => {
    const { rerender } = render(<Reviews reviews={[]} />);
    expect(screen.getByText(/No reviews yet/i)).toBeInTheDocument();
    const reviews = [{
      review_id: 1,
      author_name: 'Alice',
      text: 'Great!',
      created_at: Date.now(),
      seller_response: {
        author_name: 'Seller',
        text: 'Thanks!',
        created_at: Date.now(),
      },
    }];
    rerender(<Reviews reviews={reviews} />);
    expect(screen.getByText('Alice')).toBeInTheDocument();
    expect(screen.getByText('Great!')).toBeInTheDocument();
    expect(screen.getByText(/Seller:/i)).toBeInTheDocument();
    expect(screen.getByText('Thanks!')).toBeInTheDocument();
  });

  it('SellerProductCard renders and triggers click', () => {
    const onClick = jest.fn();
    const product = { name: 'Alpha', price: 10, image_url: '/alpha.png', category_name: 'Cat A' };
    render(<SellerProductCard product={product} onClick={onClick} />);
    expect(screen.getByText('Alpha')).toBeInTheDocument();
    expect(screen.getByText(/Price: \$10/)).toBeInTheDocument();
    fireEvent.click(screen.getByText('Alpha'));
    expect(onClick).toHaveBeenCalled();
  });
});
