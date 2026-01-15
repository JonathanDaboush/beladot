/**
 * OrderAddressForm Component
 *
 * Displays a form for entering order address details (address, postal code, country, city).
 * Handles field changes and notifies parent via onChange prop.
 *
 * Props:
 *   - onChange: Function to call when form fields change
 */
import React, { useState } from 'react';

/**
 * Main order address form component.
 */
const OrderAddressForm = ({ onChange }) => {
  const [fields, setFields] = useState({
    address: '',
    postal_code: '',
    country: '',
    city: ''
  });

  /**
   * Handles input changes and updates parent via onChange.
   */
  const handleChange = (e) => {
    const { name, value } = e.target;
    const updated = { ...fields, [name]: value };
    setFields(updated);
    if (onChange) onChange(updated);
  };

  return (
    <div className="order-address-form">
      <label>
        Address:
        <input name="address" value={fields.address} onChange={handleChange} required />
      </label>
      <label>
        Postal Code:
        <input name="postal_code" value={fields.postal_code} onChange={handleChange} required />
      </label>
      <label>
        Country:
        <input name="country" value={fields.country} onChange={handleChange} required />
      </label>
      <label>
        City:
        <input name="city" value={fields.city} onChange={handleChange} required />
      </label>
    </div>
  );
};

export default OrderAddressForm;
