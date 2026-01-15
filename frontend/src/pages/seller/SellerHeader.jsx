// Moved from src/seller
import React from 'react';
import { NavLink } from 'react-router-dom';
import './SellerHeader.css';

export default function SellerHeader() {
  return (
    <header className="seller-header">
      <nav>
        <ul className="seller-nav">
          <li><NavLink to="/seller/products" activeClassName="active">Products</NavLink></li>
          <li><NavLink to="/seller/analysis" activeClassName="active">Analysis</NavLink></li>
          <li><NavLink to="/seller/payments" activeClassName="active">Seller Payments</NavLink></li>
        </ul>
      </nav>
    </header>
  );
}
