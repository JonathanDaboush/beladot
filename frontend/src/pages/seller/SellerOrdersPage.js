import React from 'react';
import PageHeader from '../../components/PageHeader';
import EmptyState from '../../components/EmptyState';

const SellerOrdersPage = () => (
  <div>
    <PageHeader title="Orders" subtitle="Monitor and fulfill incoming orders" />
    <EmptyState
      title="No orders yet"
      explanation="New orders will appear here. Promote your products to drive sales."
      icon={"🧾"}
    />
  </div>
);

export default SellerOrdersPage;
