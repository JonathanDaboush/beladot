// Moved from src/seller
import React, { useState } from 'react';
import './SellerAnalysis.css';

export default function SellerAnalysis() {
  // TODO: Fetch analysis data and implement controls
  return (
    <div className="seller-analysis-page">
      <div className="analysis-left">
        {/* TODO: Insert chart/graph here */}
      </div>
      <div className="analysis-right">
        <input type="text" placeholder="Search products..." />
        {/* TODO: Analysis options and filters */}
      </div>
      <div className="analysis-summary">
        <span>Min: {/* TODO */}</span>
        <span>Max: {/* TODO */}</span>
        <span>Avg: {/* TODO */}</span>
      </div>
    </div>
  );
}
