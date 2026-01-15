import React, { useEffect, useState } from 'react';
import { getShipmentEvents } from '../../api/shipmentService';

const ShipmentEventsPage = ({ onSelect }) => {
  const [events, setEvents] = useState([]);
  useEffect(() => {
    getShipmentEvents().then(setEvents);
  }, []);
  return (
    <div className="shipment-events-page">
      <h2>Shipment Events</h2>
      <div className="shipment-events-list">
        {events.map(event => (
          <div className="shipment-event-item" key={event.event_id} onClick={() => onSelect(event)}>
            <div><b>Order #:</b> {event.order_number}</div>
            <div><b>Status:</b> {event.status}</div>
            <div><b>Location:</b> {event.location}</div>
            <div><b>Created:</b> {event.created_at}</div>
          </div>
        ))}
      </div>
    </div>
  );
};
export default ShipmentEventsPage;
