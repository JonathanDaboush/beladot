// Moved from src/seller
import React, { useState } from 'react';
import './SellerAnalysis.css';
import PageHeader from '../../components/PageHeader';
import EmptyState from '../../components/EmptyState';

export default function SellerAnalysis() {
  // TODO: Fetch analysis data and implement controls
  return (
    <div className="seller-analysis-page">
      <PageHeader title="Analytics" subtitle="Track performance and trends" />
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
      <EmptyState
        title="No analytics data yet"
        explanation="Data will appear once you have sales and interactions."
        icon={"📈"}
      />
    </div>
  );
}
