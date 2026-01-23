import React, { useEffect, useState, memo } from 'react';
import { getShipments } from '../../api/shipmentService';
import PageHeader from '../../components/PageHeader';
import EmptyState from '../../components/EmptyState';

const ShipmentsList = memo(({ shipments, onSelect }) => (
  <div className="shipments-list">
    {shipments.map(shipment => (
      <div className="shipment-item" key={shipment.shipment_id} onClick={() => onSelect(shipment)}>
        <div><b>Order Date:</b> {shipment.order_date}</div>
        <div><b>Address:</b> {shipment.country}, {shipment.province}, {shipment.city}, {shipment.address} {shipment.postal_code}</div>
        <div><b>Status:</b> {shipment.shipment_status}</div>
      </div>
    ))}
  </div>
));

const ShipmentsPage = ({ onSelect }) => {
  const [shipments, setShipments] = useState([]);
  useEffect(() => {
    getShipments().then(setShipments);
  }, []);
  return (
    <div className="shipments-page">
      <PageHeader title="Shipments" subtitle="Track shipments and statuses" />
      {shipments.length === 0 ? (
        <EmptyState
          title="No shipments found"
          explanation="When shipments are in progress or completed, they will appear here."
          icon={"🚚"}
        />
      ) : (
        <ShipmentsList shipments={shipments} onSelect={onSelect} />
      )}
    </div>
  );
};
export default ShipmentsPage;
