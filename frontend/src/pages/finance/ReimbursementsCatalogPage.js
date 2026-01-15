/**
 * ReimbursementsCatalogPage
 *
 * Displays a catalog of finance reimbursements for employees.
 * Fetches data using a custom hook and displays each reimbursement in a card format.
 * Allows navigation to individual reimbursement detail pages.
 *
 * Usage:
 * Route: /finance/reimbursements
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import useFinanceReimbursements from '../../hooks/useFinanceReimbursements';

/**
 * Main component for displaying a list of finance reimbursements.
 */
const ReimbursementsCatalogPage = () => {
  const { data: reimbursements, loading, error } = useFinanceReimbursements();
  const navigate = useNavigate();

  return (
    <div className="container py-4">
      {/* Page Title */}
      <h2 className="mb-4">Finance Reimbursements</h2>
      {/* Conditional rendering for loading, error, and empty states */}
      {loading ? (
        <div className="alert alert-info">Loading...</div>
      ) : error ? (
        <div className="alert alert-danger">{error}</div>
      ) : reimbursements.length === 0 ? (
        <div className="alert alert-warning">No data available</div>
      ) : (
        <div className="row row-cols-1 row-cols-md-2 g-4">
          {/* Render each reimbursement as a card */}
          {reimbursements.map(r => (
            <div key={r.reimbursement_id} className="col">
              <div className="card h-100 shadow-sm" role="button" onClick={() => navigate(`/finance/reimbursements/${r.reimbursement_id}`)}>
                <div className="card-body">
                  <div><strong>Employee:</strong> {r.employee_name}</div>
                  <div><strong>Status:</strong> {r.status}</div>
                  <div><strong>Date of Incident:</strong> {r.date}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ReimbursementsCatalogPage;
