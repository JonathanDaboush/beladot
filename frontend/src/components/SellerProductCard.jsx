import React from 'react';
import './SellerProductCard.css';

export default function SellerProductCard({ product, onClick }) {
  return (
    <div className="seller-product-card" onClick={onClick}>
      <img src={product.image_url} alt={product.name} className="product-image" />
      <div className="product-info">
        <h3>{product.name}</h3>
        <p>Price: ${product.price}</p>
        <p>Category: {product.category_name}</p>
      </div>
    </div>
  );
}
