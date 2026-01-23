import React, { useEffect, useState } from 'react';
import { getShipmentGrievanceReports } from '../../api/customerService';
import PageHeader from '../../components/PageHeader';
import EmptyState from '../../components/EmptyState';
import Button from '../../components/Button';

const ShipmentIssuesPage = ({ onSelect }) => {
  const [issues, setIssues] = useState([]);
  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        const result = await getShipmentGrievanceReports();
        if (mounted) setIssues(result || []);
      } catch {
        if (mounted) setIssues([]);
      }
    })();
    return () => { mounted = false; };
  }, []);
  return (
    <div className="shipment-issues-page">
      <PageHeader title="Shipment Issues" subtitle="Track and process shipment grievances" />
      <div className="shipment-issues-list">
        {issues.length === 0 ? (
          <EmptyState
            title="No shipment issues"
            explanation="There are currently no open shipment issues."
            action={<Button kind="primary" onClick={() => window.location.href = '/'}>Go to dashboard</Button>}
          />
        ) : (
          issues.map(issue => (
            <div className="shipment-issue-item" key={issue.issue_id} onClick={() => onSelect(issue)}>
              <div><b>Type:</b> {issue.issue_type}</div>
              <div><b>Status:</b> {issue.shipment_status}</div>
              <div><b>Created:</b> {issue.created_at}</div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
export default ShipmentIssuesPage;
