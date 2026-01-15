/**
 * Pagination Component
 *
 * Renders pagination controls for navigating between pages of data.
 * Allows changing page size and navigating to previous/next pages.
 *
 * Props:
 *   - page: Current page number
 *   - pageSize: Number of items per page
 *   - total: Total number of items
 *   - onPageChange: Function to call when the page changes
 *   - onPageSizeChange: Function to call when the page size changes
 */
import React from 'react';
import './Pagination.css';

/**
 * Main pagination controls component.
 */
const Pagination = ({ page, pageSize, total, onPageChange, onPageSizeChange }) => {
  const pageCount = Math.ceil(total / pageSize);
  if (pageCount <= 1) return null;
  const pages = Array.from({ length: pageCount }, (_, i) => i + 1);

  return (
    <div className="pagination-controls">
      {/* Page size selector */}
      <select value={pageSize} onChange={e => onPageSizeChange(Number(e.target.value))} className="page-size-selector">
        <option value={25}>25</option>
        <option value={50}>50</option>
      </select>
      {/* Previous page button */}
      <button disabled={page === 1} onClick={() => onPageChange(page - 1)} className="page-btn">Previous</button>
      {/* Page number buttons */}
      {pages.map(p => (
        <button
          key={p}
          className={`page-btn${p === page ? ' active' : ''}`}
          onClick={() => onPageChange(p)}
        >
          {p}
        </button>
      ))}
      {/* Next page button */}
      <button disabled={page === pageCount} onClick={() => onPageChange(page + 1)} className="page-btn">Next</button>
    </div>
  );
};

export default Pagination;
