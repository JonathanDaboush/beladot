/**
 * ReimbursementDetailPage
 *
 * This page displays detailed information about a single reimbursement, including linked issue and employee details.
 * Allows editing and deleting the reimbursement. Data is fetched via a custom hook.
 *
 * Features:
 * - View reimbursement details
 * - Edit reimbursement information
 * - Delete reimbursement and redirect
 * - View linked issue and employee details
 *
 * Usage:
 * Route: /finance/reimbursements/:id
 */
import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import useFinanceReimbursementDetail from '../../hooks/useFinanceReimbursementDetail';

/**
 * Main component for displaying and editing a reimbursement.
 */
const ReimbursementDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: reimbursement, loading, error } = useFinanceReimbursementDetail(id);
  const [editMode, setEditMode] = useState(false);
  const [form, setForm] = useState({});
  const [submitLoading, setSubmitLoading] = useState(false);


  // Update form state when reimbursement data is loaded
  React.useEffect(() => {
    if (reimbursement) setForm(reimbursement);
  }, [reimbursement]);

  // --- Handlers ---

  /**
   * Handles input changes for the edit form.
   * @param {object} e - Input change event
   */
  const handleChange = e => {
    const { name, value } = e.target;
    setForm(f => ({ ...f, [name]: value }));
  };

  /**
   * Enables edit mode for the reimbursement form.
   */
  const handleEdit = () => setEditMode(true);

  /**
   * Cancels edit mode and resets form.
   */
  const handleCancel = () => setEditMode(false);

  /**
   * Submits the edited reimbursement data.
   * Simulates API call with setTimeout.
   */
  const handleSubmit = async () => {
    setSubmitLoading(true);
    // TODO: Replace with real API call
    setTimeout(() => {
      setEditMode(false);
      setSubmitLoading(false);
    }, 1000);
  };

  /**
   * Deletes the reimbursement and redirects to the reimbursements catalog.
   * Simulates API call with setTimeout.
   */
  const handleDelete = async () => {
    setSubmitLoading(true);
    // TODO: Replace with real API call
    setTimeout(() => {
      navigate('/finance/reimbursements');
    }, 1000);
  };

  // --- Conditional rendering for loading, error, and not found states ---
  if (loading || submitLoading) return <div className="container py-4"><div className="alert alert-info">Loading...</div></div>;
  if (error) return <div className="container py-4"><div className="alert alert-danger">{error}</div></div>;
  if (!reimbursement) return <div className="container py-4"><div className="alert alert-warning">Not found</div></div>;

  // --- Main render ---
  return (
    <div className="container py-4">
      {/* Page Title */}
      <h2 className="mb-4">Reimbursement Detail</h2>

      {/* Reimbursement Information Card */}
      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <h3 className="card-title mb-3">Reimbursement Information</h3>
          {editMode ? (
            <form onSubmit={e => { e.preventDefault(); handleSubmit(); }}>
              {/* Editable fields */}
              <div className="mb-3">
                <label className="form-label">Amount</label>
                <input name="amount" type="number" value={form.amount} onChange={handleChange} className="form-control" />
              </div>
              <div className="mb-3">
                <label className="form-label">Status</label>
                <input name="status" value={form.status} onChange={handleChange} className="form-control" />
              </div>
              <div className="mb-3">
                <label className="form-label">Date</label>
                <input name="date" value={form.date} onChange={handleChange} className="form-control" />
              </div>
              <div className="mb-3">
                <label className="form-label">Description</label>
                <textarea name="description" value={form.description} onChange={handleChange} className="form-control" />
              </div>
              {/* Form action buttons */}
              <button type="button" className="btn btn-secondary me-2" onClick={handleCancel}>Cancel</button>
              <button type="submit" className="btn btn-primary">Submit</button>
            </form>
          ) : (
            <>
              {/* Display reimbursement details */}
              <div className="mb-2"><strong>Amount:</strong> {reimbursement.amount}</div>
              <div className="mb-2"><strong>Status:</strong> {reimbursement.status}</div>
              <div className="mb-2"><strong>Date:</strong> {reimbursement.date}</div>
              <div className="mb-2"><strong>Description:</strong> {reimbursement.description}</div>
              {/* Edit and Delete buttons */}
              <button className="btn btn-outline-primary me-2" onClick={handleEdit}>Edit</button>
              <button className="btn btn-outline-danger" onClick={handleDelete}>Delete</button>
            </>
          )}
        </div>
      </div>

      {/* Linked Issue Information Card */}
      <div className="card mb-4">
        <div className="card-body">
          <h4 className="card-title mb-3">Linked Issue Information</h4>
          <div className="mb-2"><strong>Description:</strong> {reimbursement.issue?.description}</div>
          <div className="mb-2"><strong>Cost:</strong> {reimbursement.issue?.cost}</div>
          <div className="mb-2"><strong>Date:</strong> {reimbursement.issue?.date}</div>
          <div className="mb-2"><strong>Status:</strong> {reimbursement.issue?.status}</div>
        </div>
      </div>

      {/* Employee Information Card */}
      <div className="card">
        <div className="card-body">
          <h4 className="card-title mb-3">Employee Information</h4>
          <div className="mb-2"><strong>Name:</strong> {reimbursement.employee?.name}</div>
          <div className="mb-2"><strong>Date of Birth:</strong> {reimbursement.employee?.dob}</div>
          <div className="mb-2"><strong>Phone:</strong> {reimbursement.employee?.phone}</div>
          <div className="mb-2"><strong>Email:</strong> {reimbursement.employee?.email}</div>
          <div>
            {/* Employee image if available */}
            {reimbursement.employee?.image && (
              <img src={reimbursement.employee?.image} alt="Employee" className="img-thumbnail mt-2" style={{ maxWidth: 120 }} />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
export default ReimbursementDetailPage;
