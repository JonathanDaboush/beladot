import React, { useEffect, useState } from 'react';
import { getShipmentGrievanceReports } from '../../api/customerService';

const ShipmentIssuesPage = ({ onSelect }) => {
  const [issues, setIssues] = useState([]);
  useEffect(() => {
    getShipmentGrievanceReports().then(setIssues);
  }, []);
  return (
    <div className="shipment-issues-page">
      <h2>Shipment Issues</h2>
      <div className="shipment-issues-list">
        {issues.map(issue => (
          <div className="shipment-issue-item" key={issue.issue_id} onClick={() => onSelect(issue)}>
            <div><b>Type:</b> {issue.issue_type}</div>
            <div><b>Status:</b> {issue.shipment_status}</div>
            <div><b>Created:</b> {issue.created_at}</div>
          </div>
        ))}
      </div>
    </div>
  );
};
export default ShipmentIssuesPage;
