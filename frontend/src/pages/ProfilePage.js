import React, { useState, useEffect } from 'react';
import './ProfilePage.css';

const ProfilePage = () => {
  const [user, setUser] = useState(null);
  const [editMode, setEditMode] = useState({ user: false, shipping: false, payment: false });
  const [form, setForm] = useState({});

  useEffect(() => {
    fetch('/api/profile')
      .then(res => res.json())
      .then(data => {
        setUser(data.user);
        setForm(data.user);
      });
  }, []);

  const handleEdit = section => setEditMode({ ...editMode, [section]: true });
  const handleCancel = section => {
    setEditMode({ ...editMode, [section]: false });
    setForm(user);
  };
  const handleSave = section => {
    // Save changes to backend
    fetch(`/api/profile/${section}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    }).then(() => {
      setEditMode({ ...editMode, [section]: false });
      setUser(form);
    });
  };

  if (!user) return <div className="profile-loading">Loading...</div>;

  return (
    <div className="profile-page">
      <h2>Profile</h2>
      <section className="profile-section">
        <h3>User Information</h3>
        {editMode.user ? (
          <>
            <input value={form.full_name || ''} onChange={e => setForm({ ...form, full_name: e.target.value })} />
            <button onClick={() => handleSave('user')}>Save</button>
            <button onClick={() => handleCancel('user')}>Cancel</button>
          </>
        ) : (
          <>
            <div>Name: {user.full_name}</div>
            <button onClick={() => handleEdit('user')}>Edit</button>
          </>
        )}
      </section>
      <section className="profile-section">
        <h3>Shipping Information</h3>
        {user.shipping ? (
          editMode.shipping ? (
            <>
              <input value={form.shipping || ''} onChange={e => setForm({ ...form, shipping: e.target.value })} />
              <button onClick={() => handleSave('shipping')}>Save</button>
              <button onClick={() => handleCancel('shipping')}>Cancel</button>
            </>
          ) : (
            <>
              <div>{user.shipping}</div>
              <button onClick={() => handleEdit('shipping')}>Edit</button>
            </>
          )
        ) : (
          <button onClick={() => handleEdit('shipping')}>Create</button>
        )}
      </section>
      <section className="profile-section">
        <h3>Payment Information</h3>
        {user.payment ? (
          editMode.payment ? (
            <>
              <input value={form.payment || ''} onChange={e => setForm({ ...form, payment: e.target.value })} />
              <button onClick={() => handleSave('payment')}>Save</button>
              <button onClick={() => handleCancel('payment')}>Cancel</button>
            </>
          ) : (
            <>
              <div>{user.payment}</div>
              <button onClick={() => handleEdit('payment')}>Edit</button>
            </>
          )
        ) : (
          <button onClick={() => handleEdit('payment')}>Create</button>
        )}
      </section>
      <button className="delete-account-btn" onClick={async () => {
        const res = await fetch('/api/disable_user_account', { method: 'POST' });
        if (res.status === 401 || res.status === 403) {
          alert('Unauthorized or forbidden');
          return;
        }
        window.location.href = '/login';
      }}>Delete Account</button>
    </div>
  );
};

export default ProfilePage;
