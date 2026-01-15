/**
 * CatalogPage Component
 *
 * Renders a paginated catalog of items using a reusable, memoized ProductList subcomponent.
 * Handles empty state, pagination controls, and delegates item rendering to a renderSummary prop.
 *
 * Props:
 *   - items: Array of catalog items to display
 *   - onItemClick: Function to call when an item is clicked
 *   - renderSummary: Function to render a summary for each item
 *   - emptyText: Text to display if no items are present
 *   - page: Current page number (1-based)
 *   - pageSize: Number of items per page
 *   - onPageChange: Function to call when the page changes
 */
import React, { memo, useMemo } from 'react';

/**
 * Main catalog page component. Handles pagination and delegates list rendering.
 */
const CatalogPage = ({ items, onItemClick, renderSummary, emptyText = 'No items available', page = 1, pageSize = 25, onPageChange }) => {
  // Calculate the starting index for the current page
  const startIdx = (page - 1) * pageSize;
  // Memoize the paged items to avoid unnecessary recalculations
  const pagedItems = useMemo(() => items.slice(startIdx, startIdx + pageSize), [items, startIdx, pageSize]);
  const totalPages = Math.ceil(items.length / pageSize);

  return (
    <div className="container-fluid px-0">
      {/* Render empty state if no items, otherwise render the paginated product list */}
      {pagedItems.length === 0 ? (
        <div className="alert alert-secondary text-center">{emptyText}</div>
      ) : (
        <ProductList items={pagedItems} onItemClick={onItemClick} renderSummary={renderSummary} />
      )}
      {/* Pagination controls */}
      {totalPages > 1 && (
        <div className="d-flex justify-content-center gap-2 mt-4">
          {page > 1 && (
            <button className="btn btn-outline-primary" onClick={() => onPageChange(page - 1)}>Previous</button>
          )}
          {page < totalPages && (
            <button className="btn btn-outline-primary" onClick={() => onPageChange(page + 1)}>Next</button>
          )}
        </div>
      )}
    </div>
  );
};

/**
 * ProductList Subcomponent
 *
 * Memoized for performance. Renders a grid of catalog items.
 * Each item is clickable and delegates summary rendering to the parent.
 *
 * Props:
 *   - items: Array of items to display
 *   - onItemClick: Function to call when an item is clicked
 *   - renderSummary: Function to render a summary for each item
 */
const ProductList = memo(({ items, onItemClick, renderSummary }) => (
  <div className="row g-3">
    {items.map((item, idx) => (
      <div
        key={item.id || idx}
        className="col-md-6 col-lg-4"
        onClick={() => onItemClick(item)}
        tabIndex={0}
        role="button"
        style={{ cursor: 'pointer' }}
      >
        {renderSummary(item)}
      </div>
    ))}
  </div>
));

export default CatalogPage;
