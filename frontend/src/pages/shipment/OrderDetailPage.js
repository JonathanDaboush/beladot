import React, { useEffect, useState } from 'react';
import { getOrderDetails, createShipmentEvent } from '../../api/shipmentService';
import PageHeader from '../../components/PageHeader';
import Button from '../../components/Button';

const OrderDetailPage = ({ orderId }) => {
  const [detail, setDetail] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [eventData, setEventData] = useState({ status: '', description: '', location: '' });

  useEffect(() => {
    getOrderDetails(orderId).then(setDetail);
  }, [orderId]);

  if (!detail) return <div>Loading...</div>;
  const { order_items, shipment, shipment_items } = detail;

  return (
    <div className="order-detail-page">
      <PageHeader title="Order Detail" subtitle="Review order and create shipment events" />
      <div><b>Customer:</b> {shipment?.customer_name}</div>
      <div><b>Address:</b> {shipment?.address}</div>
      <div><b>Status:</b> {shipment?.shipment_status}</div>
      <div className="order-items-list">
        {order_items.map((item, idx) => (
          <div className="order-item" key={idx}>
            <div>{item.product_name}</div>
            <div>Qty: {item.quantity}</div>
          </div>
        ))}
      </div>
      <Button kind="primary" onClick={() => setShowModal(true)}>Create Shipment Event</Button>
      {showModal && (
        <div className="modal">
          <h3>Create Shipment Event</h3>
          <input placeholder="Status" value={eventData.status} onChange={e => setEventData({ ...eventData, status: e.target.value })} />
          <input placeholder="Description" value={eventData.description} onChange={e => setEventData({ ...eventData, description: e.target.value })} />
          <input placeholder="Location" value={eventData.location} onChange={e => setEventData({ ...eventData, location: e.target.value })} />
          <Button kind="primary" onClick={async () => {
            await createShipmentEvent(orderId, eventData);
            setShowModal(false);
          }}>Create Shipment Event</Button>
          <Button kind="secondary" onClick={() => setShowModal(false)}>Cancel</Button>
        </div>
      )}
    </div>
  );
};
export default OrderDetailPage;
