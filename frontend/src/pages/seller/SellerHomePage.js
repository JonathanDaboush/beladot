import React from 'react';
import InfoBox from '../../components/InfoBox';

const infoBoxes = [
  {
    title: 'Welcome to the Seller Portal',
    text: 'Manage your products, view orders, and track payouts all in one place.'
  },
  {
    title: 'Product Management',
    text: 'Add, edit, or remove products from your catalog. Keep your listings up to date.'
  },
  {
    title: 'Order Tracking',
    text: 'Monitor incoming orders and update their status as you fulfill them.'
  },
  {
    title: 'Payouts & Reviews',
    text: 'Track your payouts and respond to customer reviews to build your reputation.'
  }
];

const SellerHomePage = () => (
  <div>
    <h2>Seller Home</h2>
    {infoBoxes.map((box, i) => (
      <InfoBox key={i} title={box.title} text={box.text} />
    ))}
  </div>
);

export default SellerHomePage;
