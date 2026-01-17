import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import OrderAddressForm from '../OrderAddressForm';

describe('OrderAddressForm', () => {
  test('updates fields and calls onChange', async () => {
    const onChange = jest.fn();
    render(<OrderAddressForm onChange={onChange} />);

    await userEvent.type(screen.getByLabelText('Address:'), '123 Main St');
    await userEvent.type(screen.getByLabelText('Postal Code:'), '90210');
    await userEvent.type(screen.getByLabelText('Country:'), 'USA');
    await userEvent.type(screen.getByLabelText('City:'), 'LA');

    expect(onChange).toHaveBeenCalled();
    const lastCall = onChange.mock.calls.at(-1)[0];
    expect(lastCall).toMatchObject({ address: '123 Main St', postal_code: '90210', country: 'USA', city: 'LA' });
  });

  test('inputs are required', () => {
    render(<OrderAddressForm />);
    const inputs = screen.getAllByRole('textbox');
    inputs.forEach(input => expect(input).toHaveAttribute('required'));
  });
});
