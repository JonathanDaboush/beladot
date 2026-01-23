
import React, { useEffect, useState } from 'react';
import { getGrievanceDetails, processShipmentReport } from '../../api/customerService';
import DecisionFrame from '../../components/DecisionFrame';
import PageHeader from '../../components/PageHeader';
import Button from '../../components/Button';
import Toast from '../../components/Toast';

const ShipmentIssueDetailPage = ({ issueId }) => {
  const [detail, setDetail] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [faultType, setFaultType] = useState('');
  const [preview, setPreview] = useState('');
  const [toast, setToast] = useState({ open: false, kind: 'success', message: '' });

  useEffect(() => {
    getGrievanceDetails(issueId).then(setDetail);
  }, [issueId]);

  if (!detail) return <div>Loading...</div>;
  const { shipment_issue, shipment, shipment_items } = detail;

  const handlePreview = () => {
    setPreview(
      <div>
        <div><b>Selected Fault Type:</b> {faultType}</div>
      </div>
    );
  };

  return (
    <div className="shipment-issue-detail-page">
      <PageHeader title="Shipment Issue" subtitle="Review shipment and categorize fault" />
      <div><b>Type:</b> {shipment_issue?.issue_type}</div>
      <div><b>Status:</b> {shipment?.shipment_status}</div>
      <div><b>Customer:</b> {shipment?.customer_name}</div>
      <div><b>Order #:</b> {shipment?.order_number}</div>
      <div className="shipment-items-slideshow">
        {shipment_items.map((item, idx) => (
          <div className="shipment-item-slide" key={idx}>
            <img src={item.product_image} alt={item.product_name} />
            <div>{item.product_name}</div>
            <div>{item.variant_name && `Variant: ${item.variant_name}`}</div>
            <div>Qty: {item.quantity}</div>
            <div>Status: {item.status}</div>
          </div>
        ))}
      </div>
      <Button kind="primary" onClick={() => setShowModal(true)}>Process shipment issue</Button>
      <DecisionFrame
        visible={showModal}
        onCancel={() => { setShowModal(false); setPreview(''); }}
        onConfirm={async () => {
          await processShipmentReport(issueId, faultType);
          setShowModal(false);
          setPreview('');
          setToast({ open: true, kind: 'success', message: 'Shipment issue processed' });
        }}
        preview={preview}
        banner="Process Shipment Issue"
      >
        <h3>Process Shipment Issue</h3>
        <select value={faultType} onChange={e => { setFaultType(e.target.value); handlePreview(); }}>
          <option value="">Select Fault Type</option>
          <option value="broken_upon_arrival">Broken Upon Arrival</option>
          <option value="damage_in_shipping">Damage in Shipping</option>
          <option value="logistics_fault">Logistics Fault</option>
        </select>
      </DecisionFrame>
      <Toast open={toast.open} kind={toast.kind} message={toast.message} onClose={() => setToast({ ...toast, open: false })} />
    </div>
  );
};
export default ShipmentIssueDetailPage;
