import React from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import './SellerServicesLayout.css';
import { useAuth } from '../../context/AuthContext';

const navOptions = [
  { label: 'Home', to: '/seller' },
  { label: 'Products', to: '/seller/products' },
  { label: 'Orders', to: '/seller/orders' },
  { label: 'Payouts', to: '/seller/payouts' },
  { label: 'Reviews', to: '/seller/reviews' },
  { label: 'Profile', to: '/seller/profile' },
];

const SellerServicesLayout = () => {
  const { user } = useAuth();
  // Optionally filter navOptions based on seller info if needed (no frontend inference)

  return (
    <div className="seller-layout">
      <aside className="seller-sidebar">
        <nav>
          <ul>
            {navOptions.map(opt => (
              <li key={opt.to}>
                <NavLink to={opt.to} className={({ isActive }) => isActive ? 'active' : ''} end>
                  {opt.label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
        {user?.sellerName && <div className="sidebar-info">Seller: {user.sellerName}</div>}
      </aside>
      <main className="seller-main">
        <Outlet />
      </main>
    </div>
  );
};

export default SellerServicesLayout;
