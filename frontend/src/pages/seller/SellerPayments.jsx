// Moved from src/seller
import React, { useState } from 'react';
import './SellerPayments.css';

export default function SellerPayments() {
  const [year, setYear] = useState('');
  const [month, setMonth] = useState('');
  const [payouts, setPayouts] = useState([]);

  const handleSearch = () => {
    // TODO: Fetch payouts for year/month
  };

  return (
    <div className="seller-payments-page">
      <h2>Seller Payments</h2>
      <div className="payout-controls">
        <input type="number" placeholder="Year" value={year} onChange={e => setYear(e.target.value)} />
        <input type="number" placeholder="Month" value={month} onChange={e => setMonth(e.target.value)} />
        <button onClick={handleSearch}>Get Payouts</button>
      </div>
      <div className="payout-list">
        {payouts.map((payout, idx) => (
          <div key={idx} className="payout-card">
            {Object.entries(payout).map(([key, value]) => (
              key !== 'payout_id' && key !== 'seller_id' ? <div key={key}><b>{key}:</b> {value}</div> : null
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
