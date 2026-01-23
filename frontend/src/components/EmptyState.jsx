import React from 'react';

export default function EmptyState({ title, explanation, action, icon }) {
  return (
    <div className="empty-state">
      {icon && <div className="empty-icon" aria-hidden>{icon}</div>}
      <div className="empty-title h5">{title}</div>
      {explanation && <div className="empty-explanation muted">{explanation}</div>}
      {action && <div className="empty-action mt-2">{action}</div>}
    </div>
  );
}
