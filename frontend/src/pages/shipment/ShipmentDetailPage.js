
import React, { useEffect, useState } from 'react';
import { getShipment, getShipmentDetails, editShipmentIssue, deleteShipmentIssue } from '../../api/shipmentService';
import DecisionFrame from '../../components/DecisionFrame';
import PageHeader from '../../components/PageHeader';
import Button from '../../components/Button';

const ShipmentDetailPage = ({ shipmentId }) => {
  const [detail, setDetail] = useState(null);
  const [decisionMode, setDecisionMode] = useState(false);
  const [decisionType, setDecisionType] = useState('');
  const [issueFields, setIssueFields] = useState({});
  const [preview, setPreview] = useState('');

  useEffect(() => {
    getShipmentDetails(shipmentId).then(setDetail);
  }, [shipmentId]);

  if (!detail) return <div>Loading...</div>;
  const { shipment, shipment_items, shipment_issue } = detail;

  // Backend-powered preview (simulate for now)
  const getPreview = async (type, fields) => {
    if (type === 'edit') {
      return `Edit issue type to "${fields.issue_type}" and description to "${fields.description}".`;
    } else if (type === 'delete') {
      return 'Delete this shipment issue.';
    }
    return '';
  };

  const openDecision = async (type, fields = {}) => {
    setDecisionType(type);
    setIssueFields(fields);
    setPreview(await getPreview(type, fields));
    setDecisionMode(true);
  };

  const handleConfirm = async () => {
    if (decisionType === 'edit') {
      await editShipmentIssue(shipment_issue.issue_id, issueFields);
    } else if (decisionType === 'delete') {
      await deleteShipmentIssue(shipment_issue.issue_id);
    }
    setDecisionMode(false);
    setPreview('');
    setIssueFields({});
    // Refresh details
    getShipmentDetails(shipmentId).then(setDetail);
  };

  return (
    <div className="shipment-detail-page">
      <PageHeader title="Shipment Detail" subtitle="Review shipment information and issues" />
      <div><b>Customer:</b> {shipment?.customer_name}</div>
      <div><b>Address:</b> {shipment?.address}</div>
      <div><b>Amount Paid:</b> {shipment?.amount_paid}</div>
      <div className="shipment-items-list">
        {shipment_items.map((item, idx) => (
          <div className="shipment-item" key={idx}>
            <div>{item.product_name}</div>
            <div>Qty: {item.quantity}</div>
          </div>
        ))}
      </div>
      {shipment_issue && (
        <div className="shipment-issue-section">
          <h3>Shipment Issue</h3>
          <div>
            <div>Type: {shipment_issue.issue_type}</div>
            <div>Description: {shipment_issue.description}</div>
            <Button kind="secondary" onClick={() => openDecision('edit', { issue_type: shipment_issue.issue_type, description: shipment_issue.description })}>Edit Issue</Button>
            <Button kind="destructive" onClick={() => openDecision('delete')}>Delete Issue</Button>
          </div>
        </div>
      )}
      <DecisionFrame
        visible={decisionMode}
        onCancel={() => { setDecisionMode(false); setPreview(''); setIssueFields({}); }}
        onConfirm={handleConfirm}
        preview={preview}
        banner={decisionType === 'edit' ? 'Edit Shipment Issue' : 'Delete Shipment Issue'}
      >
        {decisionType === 'edit' && (
          <div>
            <div>Edit Issue</div>
            <input
              value={issueFields.issue_type || ''}
              onChange={async e => {
                const newFields = { ...issueFields, issue_type: e.target.value };
                setIssueFields(newFields);
                setPreview(await getPreview('edit', newFields));
              }}
              placeholder="Issue Type"
            />
            <input
              value={issueFields.description || ''}
              onChange={async e => {
                const newFields = { ...issueFields, description: e.target.value };
                setIssueFields(newFields);
                setPreview(await getPreview('edit', newFields));
              }}
              placeholder="Description"
            />
          </div>
        )}
        {decisionType === 'delete' && (
          <div>Are you sure you want to delete this shipment issue?</div>
        )}
      </DecisionFrame>
    </div>
  );
};
export default ShipmentDetailPage;
