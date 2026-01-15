
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './ReimbursementDetailPage.css';

const ReimbursementDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [reimbursement, setReimbursement] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetch(`/api/reimbursements/${id}`)
      .then(res => res.ok ? res.json() : Promise.reject('Failed to fetch reimbursement'))
      .then(data => {
        setReimbursement(data.item || null);
        setLoading(false);
      })
      .catch(e => {
        setError(e.toString());
        setLoading(false);
      });
  }, [id]);

  if (loading) return <div className="reimbursement-detail-page"><h2>Loading...</h2></div>;
  if (error) return <div className="reimbursement-detail-page"><h2>{error}</h2></div>;
  if (!reimbursement) return <div className="reimbursement-detail-page"><h2>Not found</h2></div>;

  // Authority signaling: show status badge and tooltip, hide edit/delete/amount fields if not Finance
  const isFinance = window.location.pathname.startsWith('/finance');
  const statusBadge = reimbursement.status === 'awaiting_finance_review'
    ? <span className="badge" title="Final resolution handled by Finance">Pending Finance Review</span>
    : reimbursement.status === 'approved'
      ? <span className="badge" title="Finance has approved this reimbursement">Finance Approved</span>
      : null;
  return (
    <div className="reimbursement-detail-page">
      <h2>Reimbursement Detail</h2>
      {statusBadge}
      <div className="detail-box">
        <div><strong>Employee Name:</strong> {reimbursement.employee_name}</div>
        <div><strong>Incident ID:</strong> {reimbursement.incident_id}</div>
        <div><strong>Status:</strong> {reimbursement.status}</div>
        {!isFinance ? null : reimbursement.amount_approved != null && (
          <div><strong>Approved Amount:</strong> ${reimbursement.amount_approved}</div>
        )}
        <div><strong>Description:</strong> {reimbursement.description}</div>
        <div><strong>Created:</strong> {reimbursement.created}</div>
        {/* No reimbursement ID shown */}
      </div>
      <button className="back-btn" onClick={() => navigate(-1)}>Back to List</button>
    </div>
  );
};

export default ReimbursementDetailPage;
