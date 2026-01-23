/**
 * Layout Component
 *
 * Provides the global layout for the application, including header, role-based redirect, and main content area.
 *
 * Props:
 *   - children: The main content to render inside the layout
 */
import React from 'react';
import Header from './Header';
import RoleBasedRedirect from './RoleBasedRedirect';

/**
 * Main layout component for the app.
 */
const Layout = ({ children }) => (
  <div className="global-layout">
    <Header />
    <RoleBasedRedirect />
    <main className="page" style={{ minHeight: '80vh' }}>
      {children}
    </main>
  </div>
);

export default Layout;
