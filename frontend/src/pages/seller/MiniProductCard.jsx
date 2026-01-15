// Moved from src/seller
import React from 'react';
import './MiniProductCard.css';

export default function MiniProductCard({ product, onClick }) {
  return (
    <div className="mini-product-card" onClick={onClick}>
      <img src={product.image_url} alt={product.name} />
      <div>{product.name}</div>
      <div>${product.price}</div>
    </div>
  );
}
