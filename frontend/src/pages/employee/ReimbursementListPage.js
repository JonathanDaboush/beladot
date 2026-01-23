
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import PageHeader from '../../components/PageHeader';
import EmptyState from '../../components/EmptyState';
import DepartmentContext from '../../components/DepartmentContext';
import './ReimbursementListPage.css';

const ReimbursementListPage = () => {
  const [reimbursements, setReimbursements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetch('/api/reimbursements')
      .then(res => res.ok ? res.json() : Promise.reject('Failed to fetch reimbursements'))
      .then(data => {
        setReimbursements(data.items || []);
        setLoading(false);
      })
      .catch(e => {
        setError(e.toString());
        setLoading(false);
      });
  }, []);

  return (
    <div className="reimbursement-list-page">
      <PageHeader title="Reimbursements" subtitle="Track and review reimbursement claims" />
      <DepartmentContext />
      {loading ? <div>Loading...</div> : error ? <div>{error}</div> : (
        reimbursements.length === 0 ? (
          <EmptyState
            title="No reimbursement requests"
            explanation="When reimbursement claims are submitted, they will appear here."
            icon={"🧾"}
          />
        ) : (
          <table className="reimbursement-table">
            <thead>
              <tr>
                <th>Employee Name</th>
                <th>Incident Number</th>
                <th>Status</th>
                <th>Approved Amount</th>
              </tr>
            </thead>
            <tbody>
              {reimbursements.map((r, idx) => (
                <tr key={idx} onClick={() => navigate(`/employee/reimbursement/detail/${idx}`)} className="clickable-row">
                  <td>{r.employee_name}</td>
                  <td>{r.incident_id}</td>
                  <td>{r.status}</td>
                  <td>{r.amount_approved != null ? `$${r.amount_approved}` : ''}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )
      )}
    </div>
  );
};

export default ReimbursementListPage;
