import React, { useState, useEffect } from 'react';
import './ProductPaymentsPage.css';

export default function ProductPaymentsPage() {
  const [payouts, setPayouts] = useState([]);
  useEffect(() => {
    // TODO: Fetch payouts
  }, []);
  return (
    <div className="product-payments-page">
      <h2>Product Payments</h2>
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Amount</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {payouts.map((payout, idx) => (
            <tr key={idx}>
              <td>{payout.date}</td>
              <td>${payout.amount}</td>
              <td>{payout.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
