import React, { useState } from 'react';
// ...existing code...

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    if (res.ok) {
      window.location.href = '/';
    } else {
      setError('Invalid credentials');
    }
  };

  return (
    <div className="container py-4 d-flex justify-content-center align-items-center" style={{ minHeight: '80vh' }}>
      <div className="w-100" style={{ maxWidth: '400px' }}>
        <h2 className="mb-4 text-center">Login</h2>
        <form onSubmit={handleLogin} className="card p-4 shadow-sm">
          <div className="mb-3">
            <input
              type="text"
              className="form-control"
              placeholder="Email or Username"
              value={email}
              onChange={e => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="mb-3">
            <input
              type="password"
              className="form-control"
              placeholder="Password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="btn btn-primary w-100 mb-2">Login</button>
          <button type="button" className="btn btn-link w-100 mb-1" onClick={() => window.location.href = '/forgot-password'}>Forgot Password</button>
          <button type="button" className="btn btn-link w-100" onClick={() => window.location.href = '/register'}>Create Account</button>
        </form>
        {error && <div className="alert alert-danger mt-3 text-center">{error}</div>}
      </div>
    </div>
  );
};

export default LoginPage;
