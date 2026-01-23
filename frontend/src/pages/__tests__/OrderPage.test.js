import React from 'react';
import { renderWithRouter } from '../../test-utils/renderWithRouter';
import { fireEvent } from '@testing-library/react';
import OrderPage from '../OrderPage';

describe('OrderPage', () => {
  it('renders header and submits address fields', () => {
    const onSubmit = jest.fn();
    const { getByText, getByLabelText } = renderWithRouter(<OrderPage onSubmit={onSubmit} />);

    // Header present
    expect(getByText('Order')).toBeInTheDocument();

    // Fill fields
    fireEvent.change(getByLabelText('Address:'), { target: { value: '123 Street' } });
    fireEvent.change(getByLabelText('Postal Code:'), { target: { value: '90210' } });
    fireEvent.change(getByLabelText('Country:'), { target: { value: 'USA' } });
    fireEvent.change(getByLabelText('City:'), { target: { value: 'LA' } });

    // Submit
    fireEvent.click(getByText('Place order'));

    expect(onSubmit).toHaveBeenCalledWith({ address: '123 Street', postal_code: '90210', country: 'USA', city: 'LA' });
  });
});
