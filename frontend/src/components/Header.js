
import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { usePortalType } from '../hooks/usePortalType';
import UserMenu from './UserMenu';

const Header = () => {
  const [categories, setCategories] = useState([]);
  const [search, setSearch] = useState('');
  const [dropdown, setDropdown] = useState(null);
  const { isEmployee, isSeller } = useAuth();
  const portalType = usePortalType();

  useEffect(() => {
    // Mock fetch for tests
    const fetchFn = typeof fetch !== 'undefined' ? fetch : () => Promise.resolve({ json: () => Promise.resolve({ categories: [] }) });
    fetchFn('/api/categories')
      .then(res => res.json())
      .then(data => setCategories(data.categories || []));
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    window.location.href = `/search?query=${encodeURIComponent(search)}`;
  };

  const handleLogout = () => {
    // TODO: Implement logout logic (clear session, redirect, etc.)
    window.location.href = '/logout';
  };

  return (
    <header className="header">
      <div className="header-left">
        <span className="logo">Bela</span>
      </div>
      <div className="header-center">
        {portalType === 'user' && (
          <>
            <form onSubmit={handleSearch} className="search-form">
              <input
                type="text"
                placeholder="Search products..."
                value={search}
                onChange={e => setSearch(e.target.value)}
                className="search-input"
              />
              <button type="submit" className="search-btn">Search</button>
            </form>
            <div className="category-buttons">
              {categories.map(cat => (
                <div key={cat.category_id} className="category-btn-wrapper">
                  <button
                    className="category-btn"
                    onMouseEnter={() => setDropdown(cat.category_id)}
                    onMouseLeave={() => setDropdown(null)}
                    onClick={() => window.location.href = `/category/${cat.category_id}`}
                  >
                    {cat.name}
                  </button>
                  {dropdown === cat.category_id && cat.subcategories && (
                    <div className="subcategory-dropdown">
                      {cat.subcategories.map(sub => (
                        <div
                          key={sub.subcategory_id}
                          className="subcategory-item"
                          onClick={() => window.location.href = `/subcategory/${sub.subcategory_id}`}
                        >
                          {sub.name}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </>
        )}
        {portalType === 'employee' && (
          <div className="employee-header-title">Employee Portal</div>
        )}
        {portalType === 'seller' && (
          <div className="seller-header-title">Seller Portal</div>
        )}
      </div>
      <div className="header-right">
        <UserMenu onLogout={handleLogout} />
      </div>
    </header>
  );
};

export default Header;
