import React, { useEffect, useState } from 'react';
import { getAllCustomerRefundRequests } from '../../api/customerService';

const RefundRequestsPage = ({ onSelect }) => {
  const [requests, setRequests] = useState([]);
  useEffect(() => {
    getAllCustomerRefundRequests().then(setRequests);
  }, []);
  return (
    <div className="refund-requests-page">
      <h2>Customer Refund Requests</h2>
      <div className="refund-requests-list">
        {requests.map(req => (
          <div className="refund-request-item" key={req.refund_request_id} onClick={() => onSelect(req)}>
            <div><b>Employee:</b> {req.employee_name}</div>
            <div><b>Date:</b> {req.date_of_request}</div>
            <div><b>Status:</b> {req.status}</div>
          </div>
        ))}
      </div>
    </div>
  );
};
export default RefundRequestsPage;
