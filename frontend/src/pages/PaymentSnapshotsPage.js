import React, { useState } from 'react';
import CatalogPage from '../components/CatalogPage';
import DetailPage from '../components/DetailPage';

// Example data for payment snapshots
const paymentSnapshots = [
  // { id, status, amount, created, details }
];

const PaymentSnapshotsPage = () => {
  const [selectedSnapshot, setSelectedSnapshot] = useState(null);
  const [page, setPage] = useState(1);

  const handleItemClick = (item) => {
    setSelectedSnapshot(item);
  };

  const handleBack = () => {
    setSelectedSnapshot(null);
  };

  const renderSummary = (item) => (
    <div className="payment-snapshot-summary">
      <div><strong>Status:</strong> {item.status}</div>
      <div><strong>Amount:</strong> ${item.amount}</div>
      <div><strong>Created:</strong> {item.created}</div>
    </div>
  );

  return (
    <div>
      {!selectedSnapshot ? (
        <CatalogPage
          items={paymentSnapshots}
          onItemClick={handleItemClick}
          renderSummary={renderSummary}
          page={page}
          pageSize={25}
          onPageChange={setPage}
        />
      ) : (
        <DetailPage
          item={selectedSnapshot}
          images={[]}
          variants={[]}
          selectedVariant={null}
          onVariantChange={() => {}}
          reviews={[]}
          onBack={handleBack}
        />
      )}
    </div>
  );
};

export default PaymentSnapshotsPage;
