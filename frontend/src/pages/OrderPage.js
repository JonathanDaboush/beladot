import React, { useState } from 'react';
import OrderAddressForm from '../components/OrderAddressForm';
import './OrderPage.css';

const OrderPage = ({ onSubmit }) => {
  const [addressFields, setAddressFields] = useState({});

  const handleAddressChange = (fields) => {
    setAddressFields(fields);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onSubmit) onSubmit(addressFields);
    // Add further order logic here
  };

  return (
    <div className="order-page">
      <h2>Order Details</h2>
      <form onSubmit={handleSubmit}>
        <OrderAddressForm onChange={handleAddressChange} />
        <button type="submit">Place Order</button>
      </form>
    </div>
  );
};

export default OrderPage;
