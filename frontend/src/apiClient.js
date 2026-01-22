// apiClient.js
import { v4 as uuidv4 } from 'uuid';

function handleAuthError() {
  // Remove token/session and reload to force login
  localStorage.removeItem('token');
  window.location.href = '/login';
}

function buildHeaders(options = {}) {
  const headers = new Headers(options.headers || {});
  const token = localStorage.getItem('token');
  if (token) headers.set('Authorization', `Bearer ${token}`);
  // Propagate IDs for observability
  if (!headers.get('X-Request-ID')) headers.set('X-Request-ID', uuidv4());
  if (!headers.get('X-Correlation-ID')) headers.set('X-Correlation-ID', uuidv4());
  // Default content-type for JSON
  if (!headers.get('Content-Type')) headers.set('Content-Type', 'application/json');
  return headers;
}

// Resolve API base flexibly: absolute URL via env, else same-origin path
const ENV_BASE = process.env.REACT_APP_API_BASE_URL || process.env.VITE_API_BASE_URL || '';
const SAME_ORIGIN_BASE = '/api/v1';

function resolveUrl(url) {
  // Absolute URL already
  if (url.startsWith('http://') || url.startsWith('https://')) return url;
  // Allow direct '/api...' paths (CRA proxy or same-origin backend)
  if (url.startsWith('/api')) return url;
  const base = ENV_BASE || SAME_ORIGIN_BASE;
  // If env base is absolute, prefix with it; else treat as path base
  return base.startsWith('http') ? `${base}${url}` : `${base}${url}`;
}

export async function apiRequest(url, options = {}) {
  try {
    const headers = buildHeaders(options);
    const res = await fetch(resolveUrl(url), { ...options, headers });
    if (res.status === 401 || res.status === 403) {
      handleAuthError();
      throw new Error('Unauthorized or forbidden');
    }
    if (!res.ok) {
      // Try unified error shape
      let body;
      const ct = res.headers.get('Content-Type') || '';
      if (ct.includes('application/json')) {
        body = await res.json();
        const msg = body?.error_detail?.message || body?.error || res.statusText;
        throw new Error(msg);
      } else {
        const text = await res.text();
        throw new Error(text || res.statusText);
      }
    }
    return await res.json();
  } catch (err) {
    // Optionally log error
    throw err;
  }
}
