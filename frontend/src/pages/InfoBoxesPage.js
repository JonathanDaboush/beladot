import React, { useState } from 'react';
import CatalogPage from '../components/CatalogPage';
import DetailPage from '../components/DetailPage';

// Example data for InfoBoxes
const infoBoxes = [
  // { id, title, summary, details }
];

const InfoBoxesPage = () => {
  const [selectedBox, setSelectedBox] = useState(null);
  const [page, setPage] = useState(1);

  const handleItemClick = (item) => {
    setSelectedBox(item);
  };

  const handleBack = () => {
    setSelectedBox(null);
  };

  const renderSummary = (item) => (
    <div className="info-box-summary">
      <div><strong>{item.title}</strong></div>
      <div>{item.summary}</div>
    </div>
  );

  return (
    <div>
      {!selectedBox ? (
        <CatalogPage
          items={infoBoxes}
          onItemClick={handleItemClick}
          renderSummary={renderSummary}
          page={page}
          pageSize={25}
          onPageChange={setPage}
        />
      ) : (
        <DetailPage
          item={selectedBox}
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

export default InfoBoxesPage;
