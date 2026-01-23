import React from 'react';
import { renderWithRouter } from '../../../test-utils/renderWithRouter';
import RefundRequestsPage from '../RefundRequestsPage';

jest.mock('../../../api/customerService', () => ({
  __esModule: true,
  getAllCustomerRefundRequests: jest.fn(async () => [])
}));

describe('RefundRequestsPage', () => {
  it('renders header and empty state when no requests', async () => {
    const { findByText } = renderWithRouter(<RefundRequestsPage />);
    expect(await findByText('Refund Requests')).toBeInTheDocument();
    expect(await findByText('No refund requests')).toBeInTheDocument();
    expect(await findByText('There are no refund requests at the moment.')).toBeInTheDocument();
  });
});
