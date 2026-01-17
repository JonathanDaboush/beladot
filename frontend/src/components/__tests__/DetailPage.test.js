import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import DetailPage from '../DetailPage';

describe('DetailPage', () => {
  const item = { name: 'Widget', category: 'Cat', subcategory: 'Sub', price: 10, description: 'Desc' };
  const variants = [
    { id: 1, name: 'Small', price: 9 },
    { id: 2, name: 'Large', price: 12 },
  ];

  test('shows images alert when none', () => {
    render(<DetailPage item={item} images={[]} variants={[]} selectedVariant={null} onVariantChange={() => {}} reviews={[]} onBack={() => {}} />);
    expect(screen.getByText('No images available')).toBeInTheDocument();
  });

  test('allows variant selection', async () => {
    const onVariantChange = jest.fn();
    render(<DetailPage item={item} images={["x"]} variants={variants} selectedVariant={variants[0]} onVariantChange={onVariantChange} reviews={[]} onBack={() => {}} />);
    await userEvent.click(screen.getByLabelText(/Large/));
    expect(onVariantChange).toHaveBeenCalledWith(expect.objectContaining({ id: 2 }));
  });

  test('renders reviews list and empty state', () => {
    const reviews = [{ author: 'Bob', text: 'Nice', timestamp: 'now' }];
    render(<DetailPage item={item} images={["x"]} variants={[]} selectedVariant={null} onVariantChange={() => {}} reviews={reviews} onBack={() => {}} />);
    expect(screen.getByText('Bob')).toBeInTheDocument();
  });
});
