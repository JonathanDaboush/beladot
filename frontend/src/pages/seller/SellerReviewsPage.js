import React from 'react';
import PageHeader from '../../components/PageHeader';
import EmptyState from '../../components/EmptyState';

const SellerReviewsPage = () => (
  <div>
    <PageHeader title="Reviews" subtitle="Read and respond to customer feedback" />
    <EmptyState
      title="No reviews yet"
      explanation="Reviews appear once customers start responding to your products."
      icon={"💬"}
    />
  </div>
);

export default SellerReviewsPage;
