import React, { useEffect, useState } from 'react';
import { getShipmentEvent, getShipmentDetails } from '../../api/shipmentService';

const ShipmentEventDetailPage = ({ eventId }) => {
  const [event, setEvent] = useState(null);
  const [shipmentDetail, setShipmentDetail] = useState(null);

  useEffect(() => {
    getShipmentEvent(eventId).then(setEvent);
    if (event && event.shipment_id) {
      getShipmentDetails(event.shipment_id).then(setShipmentDetail);
    }
  }, [eventId, event]);

  if (!event) return <div>Loading...</div>;

  return (
    <div className="shipment-event-detail-page">
      <h2>Shipment Event Detail</h2>
      <div><b>Order #:</b> {event.order_number}</div>
      <div><b>Status:</b> {event.status}</div>
      <div><b>Location:</b> {event.location}</div>
      <div><b>Timestamp:</b> {event.created_at}</div>
      {shipmentDetail && (
        <div className="shipment-detail-section">
          <h3>Shipment Details</h3>
          {/* Render shipment details as needed, read-only */}
        </div>
      )}
    </div>
  );
};
export default ShipmentEventDetailPage;
