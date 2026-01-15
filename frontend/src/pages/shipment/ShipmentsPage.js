import React, { useEffect, useState, memo } from 'react';
import { getShipments } from '../../api/shipmentService';

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
      <h2>Shipments</h2>
      <ShipmentsList shipments={shipments} onSelect={onSelect} />
    </div>
  );
};
export default ShipmentsPage;
