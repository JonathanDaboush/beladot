
import React, { useEffect, useState } from 'react';
import './PaymentSnapshotsPage.css';

const PaymentSnapshotsPage = () => {
  const [snapshots, setSnapshots] = useState([]);
  const [filter, setFilter] = useState('');
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetch('/api/payment_snapshots')
      .then(res => res.ok ? res.json() : Promise.reject('Failed to fetch payment snapshots'))
      .then(data => {
        setSnapshots(data.items || []);
        setLoading(false);
      })
      .catch(e => {
        setError(e.toString());
        setLoading(false);
      });
  }, []);

  const filtered = filter
    ? snapshots.filter(s => s.created.startsWith(filter))
    : snapshots;

  if (selected) {
    // Detail view
    return (
      <div className="payment-snapshots-page">
        <h2>Payment Snapshot Detail</h2>
        <div className="detail-box">
          <div><strong>Employee Name:</strong> {selected.employee_name}</div>
          <div><strong>Status:</strong> {selected.status}</div>
          <div><strong>Amount:</strong> ${selected.amount}</div>
          <div><strong>Created:</strong> {selected.created}</div>
          {/* Add more fields as needed, all read-only */}
        </div>
        <button className="back-btn" onClick={() => setSelected(null)}>Back to List</button>
      </div>
    );
  }

  return (
    <div className="payment-snapshots-page">
      <h2>Payment Snapshots</h2>
      <div className="filter-row">
        <label>Filter by Date: </label>
        <input
          type="month"
          value={filter}
          onChange={e => setFilter(e.target.value)}
        />
        <button onClick={() => setFilter('')}>Clear</button>
      </div>
      {loading ? <div>Loading...</div> : error ? <div>{error}</div> : (
        <table className="snapshots-table">
          <thead>
            <tr>
              <th>Employee Name</th>
              <th>Status</th>
              <th>Amount</th>
              <th>Creation Date</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((s, idx) => (
              <tr key={idx} onClick={() => setSelected(s)} className="clickable-row">
                <td>{s.employee_name}</td>
                <td>{s.status}</td>
                <td>${s.amount}</td>
                <td>{s.created}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default PaymentSnapshotsPage;
