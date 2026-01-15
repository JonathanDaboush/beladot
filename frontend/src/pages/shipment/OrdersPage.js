import React, { useEffect, useState } from 'react';
import { getOrders } from '../../api/shipmentService';

const OrdersPage = ({ onSelect }) => {
  const [orders, setOrders] = useState([]);
  useEffect(() => {
    getOrders().then(setOrders);
  }, []);
  return (
    <div className="orders-page">
      <h2>Orders</h2>
      <div className="orders-list">
        {orders.map(order => (
          <div className="order-item" key={order.order_number} onClick={() => onSelect(order)}>
            <div><b>Order #:</b> {order.order_number}</div>
            <div><b>Created:</b> {order.created_at}</div>
            <div><b>Status:</b> {order.order_status}</div>
          </div>
        ))}
      </div>
    </div>
  );
};
export default OrdersPage;
