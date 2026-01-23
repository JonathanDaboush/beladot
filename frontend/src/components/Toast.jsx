import React, { useEffect } from 'react';

export default function Toast({ open, kind = 'success', message, onClose, duration = 2500 }) {
  useEffect(() => {
    if (!open) return;
    const t = setTimeout(() => onClose?.(), duration);
    return () => clearTimeout(t);
  }, [open, duration, onClose]);

  if (!open) return null;
  return (
    <div className={`toast ${kind}`} role="status" aria-live="polite">
      <span className="toast-msg">{message}</span>
      <button className="toast-close" onClick={onClose} aria-label="Dismiss">×</button>
    </div>
  );
}
