import React from 'react';
import PageHeader from '../../components/PageHeader';
import EmptyState from '../../components/EmptyState';

const SellerPayoutsPage = () => (
  <div>
    <PageHeader title="Payouts" subtitle="View monthly payout summaries and transfers" />
    <EmptyState
      title="No payouts yet"
      explanation="Payouts are generated after your first completed orders."
      icon={"💸"}
    />
  </div>
);

export default SellerPayoutsPage;
