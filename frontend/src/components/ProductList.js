/**
 * ProductList Component
 *
 * Displays a list of products in a card format, including image, name, price, category, subcategory, and rating.
 * Handles empty state if no products are available.
 *
 * Props:
 *   - products: Array of product objects
 */
import React from 'react';
import './ProductList.css';

/**
 * Main product list component.
 */
const ProductList = ({ products }) => {
  if (!products || products.length === 0) {
    return <div className="product-empty">No products available</div>;
  }
  return (
    <div className="product-list">
      {products.map(product => (
        <div key={product.product_id} className="product-card">
          <img src={product.image_url} alt={product.name} className="product-image" />
          <div className="product-info">
            <div className="product-name">{product.name}</div>
            <div className="product-price">${product.price}</div>
            <div className="product-meta">
              <span className="product-category">{product.category_name}</span>
              <span className="product-subcategory">{product.subcategory_name}</span>
              <span className="product-rating">50 {product.rating}</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ProductList;
