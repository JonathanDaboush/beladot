import React from 'react';

export default function PageHeader({ title, subtitle, action }) {
  return (
    <div className="page-header">
      <div className="page-header-left">
        <h1 className="page-title h4">{title}</h1>
        {subtitle && <div className="page-subtitle muted">{subtitle}</div>}
      </div>
      <div className="page-header-right">
        {action}
      </div>
    </div>
  );
}
