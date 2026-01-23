import React from 'react';
import PageHeader from '../../components/PageHeader';
import EmptyState from '../../components/EmptyState';
import Button from '../../components/Button';

const SellerProductsPage = () => (
  <div>
    <PageHeader title="Products" subtitle="Manage your listings and availability" action={<Button kind="primary">Create Product</Button>} />
    <EmptyState
      title="No products yet"
      explanation="Add your first product to start selling."
      action={<Button kind="primary">Create Product</Button>}
      icon={"📦"}
    />
  </div>
);

export default SellerProductsPage;
