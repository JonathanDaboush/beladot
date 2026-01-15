import React, { useState } from 'react';
import './CreateReimbursementPage.css';
import DecisionFrame from '../../components/DecisionFrame';
import { useAuth } from '../../context/AuthContext';

const initialForm = {
  employeeName: '',
  incidentNumber: '',
  amount: '',
  description: '',
};

const CreateReimbursementPage = () => {
  const { manager_id } = useAuth(); // Get manager_id from auth context
  const [form, setForm] = useState(initialForm);
  const [submitted, setSubmitted] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [preview, setPreview] = useState('');

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }
  function openModal(e) {
    e.preventDefault();
    setPreview('');
    setModalOpen(true);
  }
  function handlePreview() {
    setPreview(
      `You are about to submit a reimbursement claim for Employee: ${form.employeeName}, Incident: ${form.incidentNumber}, Amount: $${form.amount}, Description: "${form.description}".`
    );
  }
  function handleConfirm() {
    // manager_id is sent automatically, not editable by user
    // TODO: Integrate with backend API, include manager_id in payload
    // await api.createIncidentReport({
    //   manager_id,
    //   employee_id: form.employeeName, // or actual employee ID
    //   description: form.description,
    //   cost: form.amount,
    //   incidentNumber: form.incidentNumber
    // });
    setSubmitted(true);
    setModalOpen(false);
    setPreview('');
  }
  function handleCancel() {
    setModalOpen(false);
    setPreview('');
  }

  return (
    <div className="create-reimbursement-page">
      <h2>Create Reimbursement Claim</h2>
      {submitted ? (
        <div className="success-message">Reimbursement claim submitted!</div>
      ) : (
        <form className="reimbursement-form" onSubmit={openModal}>
          <div>
            <label>Employee Name</label>
            <input name="employeeName" value={form.employeeName} onChange={handleChange} required />
          </div>
          <div>
            <label>Incident Number</label>
            <input name="incidentNumber" value={form.incidentNumber} onChange={handleChange} required />
          </div>
          <div>
            <label>Amount</label>
            <input name="amount" type="number" value={form.amount} onChange={handleChange} required />
          </div>
          <div>
            <label>Description</label>
            <textarea name="description" value={form.description} onChange={handleChange} required />
          </div>
          <button type="submit">Submit Claim</button>
        </form>
      )}
      <DecisionFrame
        visible={modalOpen}
        onCancel={handleCancel}
        onConfirm={handleConfirm}
        preview={preview}
      >
        <h3>Submit Reimbursement Claim</h3>
        <div>Employee: {form.employeeName}</div>
        <div>Incident: {form.incidentNumber}</div>
        <div>Amount: ${form.amount}</div>
        <div>Description: {form.description}</div>
        <div className="modal-actions">
          <button type="button" onClick={handlePreview}>Preview Submission</button>
        </div>
      </DecisionFrame>
    </div>
  );
};

export default CreateReimbursementPage;
