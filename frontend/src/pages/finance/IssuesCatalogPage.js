/**
 * IssuesCatalogPage
 *
 * This page displays a catalog of finance issues for employees.
 * Fetches data using a custom hook and displays each issue in a card format.
 * Allows navigation to individual issue detail pages.
 *
 * Usage:
 * Route: /finance/issues
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import useFinanceIssues from '../../hooks/useFinanceIssues';

/**
 * Main component for displaying a list of finance issues.
 */
const IssuesCatalogPage = () => {
  const { data: issues, loading, error } = useFinanceIssues();
  const navigate = useNavigate();

  // --- Main render ---
  return (
    <div className="container py-4">
      {/* Page Title */}
      <h2 className="mb-4">Finance Issues</h2>
      {/* Conditional rendering for loading, error, and empty states */}
      {loading ? (
        <div className="alert alert-info">Loading...</div>
      ) : error ? (
        <div className="alert alert-danger">{error}</div>
      ) : issues.length === 0 ? (
        <div className="alert alert-warning">No data available</div>
      ) : (
        <div className="row row-cols-1 row-cols-md-2 g-4">
          {/* Render each issue as a card */}
          {issues.map(issue => (
            <div key={issue.issue_id} className="col">
              <div
                className="card h-100 shadow-sm"
                role="button"
                onClick={() => navigate(`/finance/issues/${issue.issue_id}`)}
              >
                <div className="card-body">
                  <div><strong>Employee:</strong> {issue.employee_name}</div>
                  <div><strong>Date:</strong> {issue.date}</div>
                  <div><strong>Status:</strong> {issue.status}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default IssuesCatalogPage;
