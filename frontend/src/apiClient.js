// apiClient.js
function handleAuthError() {
  // Remove token/session and reload to force login
  localStorage.removeItem('token');
  window.location.href = '/login';
}

export async function apiRequest(url, options = {}) {
  try {
    const res = await fetch(url, options);
    if (res.status === 401 || res.status === 403) {
      handleAuthError();
      throw new Error('Unauthorized or forbidden');
    }
    if (!res.ok) {
      const error = await res.text();
      throw new Error(error || res.statusText);
    }
    return await res.json();
  } catch (err) {
    // Optionally log error
    throw err;
  }
}
