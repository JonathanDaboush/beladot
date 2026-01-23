import React, { useEffect, useState } from 'react';
import { getAllCustomerRefundRequests } from '../../api/customerService';
import PageHeader from '../../components/PageHeader';
import EmptyState from '../../components/EmptyState';
import Button from '../../components/Button';

const RefundRequestsPage = ({ onSelect }) => {
  const [requests, setRequests] = useState([]);
  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        const result = await getAllCustomerRefundRequests();
        if (mounted) setRequests(result || []);
      } catch {
        if (mounted) setRequests([]);
      }
    })();
    return () => { mounted = false; };
  }, []);
  return (
    <div className="refund-requests-page">
      <PageHeader title="Refund Requests" subtitle="Review customer refund submissions" />
      <div className="refund-requests-list">
        {requests.length === 0 ? (
          <EmptyState
            title="No refund requests"
            explanation="There are no refund requests at the moment."
            action={<Button kind="primary" onClick={() => window.location.href = '/'}>Go to dashboard</Button>}
          />
        ) : (
          requests.map(req => (
            <div className="refund-request-item" key={req.refund_request_id} onClick={() => onSelect(req)}>
              <div><b>Employee:</b> {req.employee_name}</div>
              <div><b>Date:</b> {req.date_of_request}</div>
              <div><b>Status:</b> {req.status}</div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
export default RefundRequestsPage;
