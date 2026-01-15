// Moved from src/seller
import React, { useEffect, useState } from 'react';
import SellerHeader from './SellerHeader';
import './SellerHome.css';

export default function SellerHome() {
  const [components, setComponents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchSellerComponents() {
      try {
        const res = await fetch('/api/seller_components');
        const data = await res.json();
        setComponents(data.result || []);
      } catch (e) {
        setComponents([]);
      }
      setLoading(false);
    }
    fetchSellerComponents();
  }, []);

  return (
    <div className="seller-home">
      <SellerHeader />
      <div className="seller-home-content">
        <h1>Welcome, Seller!</h1>
        <p>Use the navigation above to manage your products, view analytics, and check your payments.</p>
        <div className="seller-home-cards">
          {loading ? (
            <div>Loading seller components...</div>
          ) : components.length === 0 ? (
            <div>No seller components found.</div>
          ) : (
            components.map((comp, idx) => (
              <div key={idx} className="seller-component-card">
                <img src={comp.img_url} alt={comp.description} />
                <div>{comp.description}</div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
