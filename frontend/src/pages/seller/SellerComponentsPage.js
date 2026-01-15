import React, { useState } from 'react';
import CatalogPage from '../../components/CatalogPage';
import DetailPage from '../../components/DetailPage';

// Example data for seller components
const sellerComponents = [
  // { id, title, summary, details }
];

const SellerComponentsPage = () => {
  const [selectedComponent, setSelectedComponent] = useState(null);
  const [page, setPage] = useState(1);

  const handleItemClick = (item) => {
    setSelectedComponent(item);
  };

  const handleBack = () => {
    setSelectedComponent(null);
  };

  const renderSummary = (item) => (
    <div className="seller-component-summary">
      <div><strong>{item.title}</strong></div>
      <div>{item.summary}</div>
    </div>
  );

  return (
    <div>
      {!selectedComponent ? (
        <CatalogPage
          items={sellerComponents}
          onItemClick={handleItemClick}
          renderSummary={renderSummary}
          page={page}
          pageSize={25}
          onPageChange={setPage}
        />
      ) : (
        <DetailPage
          item={selectedComponent}
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

export default SellerComponentsPage;
