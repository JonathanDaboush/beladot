import React, { useState } from 'react';
import CatalogPage from '../components/CatalogPage';
import DetailPage from '../components/DetailPage';
import PageHeader from '../components/PageHeader';

// Example data structure for products
const products = [
  // { id, name, category, subcategory, price, rating, image, description, variants, reviews }
];

const ProductCatalogPage = () => {
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [page, setPage] = useState(1);

  const handleItemClick = (product) => {
    setSelectedProduct(product);
  };

  const handleBack = () => {
    setSelectedProduct(null);
  };

  const renderSummary = (product) => (
    <div className="product-summary">
      <img src={product.image} alt={product.name} className="product-summary-img" />
      <div className="product-summary-info">
        <div className="product-summary-name">{product.name}</div>
        <div className="product-summary-category">{product.category} / {product.subcategory}</div>
        <div className="product-summary-price">${product.price}</div>
        <div className="product-summary-rating">Rating: {product.rating || 'N/A'}</div>
      </div>
    </div>
  );

  return (
    <div className="page">
      <PageHeader title="Catalog" subtitle="Browse products across categories" />
      {!selectedProduct ? (
        <CatalogPage
          items={products}
          onItemClick={handleItemClick}
          renderSummary={product => (
            <div className="card h-100 shadow-sm border-0">
              <div className="row g-0 align-items-center">
                <div className="col-4">
                  <img src={product.image} alt={product.name} className="img-fluid rounded-start" />
                </div>
                <div className="col-8">
                  <div className="card-body">
                    <h5 className="card-title mb-1">{product.name}</h5>
                    <div className="text-muted small mb-1">{product.category} / {product.subcategory}</div>
                    <div className="mb-1">Price: <span className="fw-bold">${product.price}</span></div>
                    <div className="mb-1">Rating: {product.rating || 'N/A'}</div>
                  </div>
                </div>
              </div>
            </div>
          )}
          page={page}
          pageSize={25}
          onPageChange={setPage}
        />
      ) : (
        <DetailPage
          item={selectedProduct}
          images={[selectedProduct.image, ...(selectedProduct.variants?.map(v => v.image) || [])]}
          variants={selectedProduct.variants}
          selectedVariant={selectedProduct.variants?.[0]}
          onVariantChange={() => {}}
          reviews={selectedProduct.reviews}
          onBack={handleBack}
        />
      )}
    </div>
  );
};

export default ProductCatalogPage;
