import React from 'react';
import PageHeader from '../../components/PageHeader';
import EmptyState from '../../components/EmptyState';

const SellerShippingPage = () => (
  <div>
    <PageHeader title="Shipping" subtitle="Manage shipping methods and shipments" />
    <EmptyState
      title="No shipments yet"
      explanation="Shipments will appear here once orders are fulfilled."
      icon={"🚚"}
    />
  </div>
);

export default SellerShippingPage;
