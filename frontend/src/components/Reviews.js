/**
 * Reviews Component
 *
 * Displays a list of product reviews, including seller responses if available.
 * Handles empty state and formats review dates.
 *
 * Props:
 *   - reviews: Array of review objects
 */
import React from 'react';
import './Reviews.css';

/**
 * Main reviews list component.
 */
const Reviews = ({ reviews }) => {
  if (!reviews || reviews.length === 0) return <div className="reviews-empty">No reviews yet</div>;
  return (
    <div className="reviews-section">
      {reviews.map(review => (
        <div key={review.review_id} className="review-card">
          <div className="review-header">
            <span className="review-author">{review.author_name}</span>
            <span className="review-date">{new Date(review.created_at).toLocaleString()}</span>
          </div>
          <div className="review-content">{review.text}</div>
          {/* Seller response section if available */}
          {review.seller_response && (
            <div className="seller-response">
              <div className="response-header">
                <span className="response-author">Seller: {review.seller_response.author_name}</span>
                <span className="response-date">{new Date(review.seller_response.created_at).toLocaleString()}</span>
              </div>
              <div className="response-content">{review.seller_response.text}</div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default Reviews;
