import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import EmployeeNav from '../EmployeeNav';

describe('EmployeeNav', () => {
  test('renders general links', () => {
    render(
      <MemoryRouter>
        <EmployeeNav user={{ department: 'shipment' }} />
      </MemoryRouter>
    );
    expect(screen.getByText('Profile')).toBeInTheDocument();
    expect(screen.getByText('Logout')).toBeInTheDocument();
  });

  test('renders department-specific links for shipment', () => {
    render(
      <MemoryRouter>
        <EmployeeNav user={{ department: 'shipment' }} />
      </MemoryRouter>
    );
    expect(screen.getByText('Orders')).toBeInTheDocument();
    expect(screen.getByText('Shipments')).toBeInTheDocument();
    expect(screen.getByText('Shipment Events')).toBeInTheDocument();
  });

  test('does not render department links for unknown dept', () => {
    render(
      <MemoryRouter>
        <EmployeeNav user={{ department: 'unknown' }} />
      </MemoryRouter>
    );
    expect(screen.queryByText('Refund Requests')).not.toBeInTheDocument();
    expect(screen.queryByText('Orders')).not.toBeInTheDocument();
  });
});
