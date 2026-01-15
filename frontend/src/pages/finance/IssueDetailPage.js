import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import useFinanceIssueDetail from '../../hooks/useFinanceIssueDetail';

const IssueDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: issue, loading, error } = useFinanceIssueDetail(id);
  const [editMode, setEditMode] = useState(false);
  const [form, setForm] = useState({});
  const [submitLoading, setSubmitLoading] = useState(false);

  React.useEffect(() => {
    if (issue) setForm(issue);
  }, [issue]);

  function handleEdit() {
    setEditMode(true);
  }
  function handleCancel() {
    setEditMode(false);
    setForm(issue);
  }
  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }
  async function handleSubmit() {
    setSubmitLoading(true);
    await fetch(`/api/finance/issues/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    });
    setEditMode(false);
    setSubmitLoading(false);
    window.location.reload();
  }
  async function handleDelete() {
    if (!window.confirm('Are you sure you want to delete this issue?')) return;
    setSubmitLoading(true);
    await fetch(`/api/finance/issues/${id}`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ confirm: true })
    });
    setSubmitLoading(false);
    navigate('/finance/issues');
  }
  async function handleCreateReimbursement() {
    navigate(`/finance/reimbursements/create?issue_id=${id}`);
  }

  if (loading || submitLoading) return <div className="alert alert-info">Loading...</div>;
  if (error) return <div className="alert alert-danger">{error}</div>;
  if (!issue) return <div className="alert alert-warning">Not found</div>;

  return (
    <div className="container py-4">
      <h2 className="mb-4">Issue Detail</h2>
      <div className="card shadow-sm mb-4">
        <div className="card-body">
          <h3 className="card-title mb-3">Issue Information</h3>
          {editMode ? (
            <form onSubmit={e => { e.preventDefault(); handleSubmit(); }}>
              <div className="mb-3">
                <label className="form-label">Description</label>
                <input name="description" value={form.description} onChange={handleChange} className="form-control" />
              </div>
              <div className="mb-3">
                <label className="form-label">Cost</label>
                <input name="cost" type="number" value={form.cost} onChange={handleChange} className="form-control" />
              </div>
              <div className="mb-3">
                <label className="form-label">Date</label>
                <input name="date" value={form.date} onChange={handleChange} className="form-control" />
              </div>
              <div className="mb-3">
                <label className="form-label">Status</label>
                <input name="status" value={form.status} onChange={handleChange} className="form-control" />
              </div>
              <button type="button" className="btn btn-secondary me-2" onClick={handleCancel}>Cancel</button>
              <button type="submit" className="btn btn-primary">Submit</button>
            </form>
          ) : (
            <>
              <div className="mb-2"><strong>Description:</strong> {issue.description}</div>
              <div className="mb-2"><strong>Cost:</strong> {issue.cost}</div>
              <div className="mb-2"><strong>Date:</strong> {issue.date}</div>
              <div className="mb-2"><strong>Status:</strong> {issue.status}</div>
              <button className="btn btn-outline-primary me-2" onClick={handleEdit}>Edit Issue</button>
              <button className="btn btn-outline-danger me-2" onClick={handleDelete}>Delete Issue</button>
              <button className="btn btn-success" onClick={handleCreateReimbursement} disabled={!issue || issue.deleted}>Create Reimbursement</button>
            </>
          )}
        </div>
      </div>
      <div className="card shadow-sm">
        <div className="card-body">
          <h3 className="card-title mb-3">Employee Information</h3>
          <div className="mb-2"><strong>Name:</strong> {issue.employee?.name}</div>
          <div className="mb-2"><strong>Date of Birth:</strong> {issue.employee?.dob}</div>
          <div className="mb-2"><strong>Phone:</strong> {issue.employee?.phone}</div>
          <div className="mb-2"><strong>Email:</strong> {issue.employee?.email}</div>
          <div><img src={issue.employee?.image} alt="Employee" style={{ maxWidth: 120 }} className="img-thumbnail" /></div>
        </div>
      </div>
    </div>
  );
};

export default IssueDetailPage;
