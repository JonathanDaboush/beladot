import React, { useState } from 'react';
import OrderAddressForm from '../components/OrderAddressForm';
import PageHeader from '../components/PageHeader';
import Button from '../components/Button';
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
      <PageHeader title="Order" subtitle="Confirm shipping details to place your order" />
      <form onSubmit={handleSubmit}>
        <OrderAddressForm onChange={handleAddressChange} />
        <div className="mt-3">
          <Button kind="primary" type="submit">Place order</Button>
        </div>
      </form>
    </div>
  );
};

export default OrderPage;
