/**
 * DetailPage Component
 *
 * Displays detailed information about a catalog item, including images, variants, and reviews.
 * Allows variant selection and navigation back to the catalog.
 *
 * Props:
 *   - item: The main item object to display
 *   - images: Array of image URLs for the item
 *   - variants: Array of variant objects
 *   - selectedVariant: The currently selected variant
 *   - onVariantChange: Function to call when a variant is selected
 *   - reviews: Array of review objects
 *   - onBack: Function to call to navigate back to the catalog
 */
import React from 'react';
// ...existing code...

/**
 * Main detail page component for catalog items.
 */
const DetailPage = ({ item, images, variants, selectedVariant, onVariantChange, reviews, onBack }) => {
  return (
    <div className="container py-4">
      {/* Back navigation button */}
      <button className="btn btn-link mb-3" onClick={onBack}>Back to Catalog</button>
      <div className="row g-4 align-items-center">
        <div className="col-md-6">
          {/* Slideshow for images */}
          {images && images.length > 0 ? (
            <div className="d-flex flex-wrap gap-2">
              {images.map((img, idx) => (
                <img key={idx} src={img} alt={`Product ${idx}`} className="img-fluid rounded shadow" style={{maxHeight: '180px'}} />
              ))}
            </div>
          ) : (
            <div className="alert alert-secondary">No images available</div>
          )}
        </div>
        <div className="col-md-6">
          <h2>{item.name}</h2>
          <div className="text-muted mb-1">{item.category} / {item.subcategory}</div>
          <div className="fw-bold fs-5 mb-1">${selectedVariant ? selectedVariant.price : item.price}</div>
          <div className="mb-1">Rating: <span className="badge bg-warning text-dark">{item.rating || 'N/A'}</span></div>
          <div className="mb-2">{item.description}</div>
          {/* Variant selection */}
          {variants && variants.length > 0 && (
            <div className="mb-2">
              <span className="fw-bold">Variants:</span>
              <div className="d-flex flex-wrap gap-2 mt-1">
                {variants.map((variant, idx) => (
                  <label key={variant.id || idx} className="btn btn-outline-primary btn-sm">
                    <input
                      type="radio"
                      name="variant"
                      checked={selectedVariant && selectedVariant.id === variant.id}
                      onChange={() => onVariantChange(variant)}
                      className="me-1"
                    />
                    {variant.name} (${variant.price})
                  </label>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
      <div className="mt-5">
        <h3>Reviews</h3>
        {/* Reviews section */}
        {reviews && reviews.length > 0 ? (
          <div className="list-group">
            {reviews.map((review, idx) => (
              <div key={idx} className="list-group-item">
                <div className="fw-bold">{review.author}</div>
                <div>{review.text}</div>
                <div className="text-muted small">{review.timestamp}</div>
              </div>
            ))}
          </div>
        ) : (
          <div className="alert alert-secondary">No reviews yet.</div>
        )}
      </div>
    </div>
  );
};

export default DetailPage;
