import React, { useEffect, useState } from 'react';
import { getOrders } from '../../api/shipmentService';
import PageHeader from '../../components/PageHeader';
import EmptyState from '../../components/EmptyState';

const OrdersPage = ({ onSelect }) => {
  const [orders, setOrders] = useState([]);
  useEffect(() => {
    getOrders().then(setOrders);
  }, []);
  return (
    <div className="orders-page">
      <PageHeader title="Orders" subtitle="Browse and review order records" />
      {orders.length === 0 ? (
        <EmptyState
          title="No orders found"
          explanation="When orders are available, they will appear here."
          icon={"🧾"}
        />
      ) : (
        <div className="orders-list">
          {orders.map(order => (
            <div className="order-item" key={order.order_number} onClick={() => onSelect(order)}>
              <div><b>Order #:</b> {order.order_number}</div>
              <div><b>Created:</b> {order.created_at}</div>
              <div><b>Status:</b> {order.order_status}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
export default OrdersPage;
