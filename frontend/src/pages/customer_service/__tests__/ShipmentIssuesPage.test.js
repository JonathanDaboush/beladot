import React from 'react';
import { renderWithRouter } from '../../../test-utils/renderWithRouter';
import ShipmentIssuesPage from '../ShipmentIssuesPage';

jest.mock('../../../api/customerService', () => ({
  __esModule: true,
  getShipmentGrievanceReports: jest.fn(async () => [])
}));

describe('ShipmentIssuesPage', () => {
  it('renders header and empty state when no issues', async () => {
    const { findByText } = renderWithRouter(<ShipmentIssuesPage />);
    expect(await findByText('Shipment Issues')).toBeInTheDocument();
    expect(await findByText('No shipment issues')).toBeInTheDocument();
    expect(await findByText('There are currently no open shipment issues.')).toBeInTheDocument();
  });
});
