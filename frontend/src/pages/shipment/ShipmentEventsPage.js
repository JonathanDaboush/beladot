import React, { useEffect, useState } from 'react';
import { getShipmentEvents } from '../../api/shipmentService';
import PageHeader from '../../components/PageHeader';
import EmptyState from '../../components/EmptyState';

const ShipmentEventsPage = ({ onSelect }) => {
  const [events, setEvents] = useState([]);
  useEffect(() => {
    getShipmentEvents().then(setEvents);
  }, []);
  return (
    <div className="shipment-events-page">
      <PageHeader title="Shipment Events" subtitle="Monitor shipment progress and statuses" />
      {events.length === 0 ? (
        <EmptyState
          title="No shipment events"
          explanation="Shipment events will appear here as shipments progress."
          icon={"🛰️"}
        />
      ) : (
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
      )}
    </div>
  );
};
export default ShipmentEventsPage;
