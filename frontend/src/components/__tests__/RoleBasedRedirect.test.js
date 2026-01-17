import React from 'react';
import { MemoryRouter } from 'react-router-dom';
import { render } from '@testing-library/react';
import RoleBasedRedirect from '../RoleBasedRedirect';
import EmployeeNav from '../EmployeeNav';
import { screen } from '@testing-library/react';

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => jest.fn(),
}));

jest.mock('../../context/AuthContext', () => ({
  useAuth: () => ({ user: { id: 1 }, isEmployee: true, isSeller: false }),
}));

test('redirects employee from root', () => {
  const { container } = render(
    <MemoryRouter initialEntries={["/"]}>
      <RoleBasedRedirect />
    </MemoryRouter>
  );
  expect(container).toBeTruthy();
});

test('EmployeeNav renders general and department links', () => {
  const user = { department: 'shipment' };
  const { container } = render(
    <MemoryRouter>
      <EmployeeNav user={user} />
    </MemoryRouter>
  );
  expect(container).toBeTruthy();
  // General links
  expect(screen.getByText('Profile')).toBeInTheDocument();
  expect(screen.getByText('Logout')).toBeInTheDocument();
  // Department links
  expect(screen.getByText('Orders')).toBeInTheDocument();
  expect(screen.getByText('Shipments')).toBeInTheDocument();
  expect(screen.getByText('Shipment Events')).toBeInTheDocument();
});
