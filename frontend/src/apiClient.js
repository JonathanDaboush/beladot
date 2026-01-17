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

const API_BASE = '/api/v1';

export async function apiRequest(url, options = {}) {
  try {
    const headers = buildHeaders(options);
    const res = await fetch(url.startsWith('/api') ? url : `${API_BASE}${url}`, { ...options, headers });
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
