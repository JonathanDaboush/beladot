
import React, { useEffect, useState, memo } from 'react';
import { useParams } from 'react-router-dom';
import { addGuestCartItem } from '../cart/guestCart';
import { useAuth } from '../context/AuthContext';
import { addToCart as addToCartApi } from '../api/cart';
import PageHeader from '../components/PageHeader';
import Button from '../components/Button';
import Toast from '../components/Toast';
// Removed custom CSS import as Bootstrap classes are used now.

const ProductDetailPage = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [selectedVariant, setSelectedVariant] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const { user } = useAuth();
  const [toast, setToast] = useState({ open: false, kind: 'success', message: '' });

  useEffect(() => {
    fetch(`/api/product/${id}`)
      .then(res => res.json())
      .then(data => {
        setProduct(data.product);
        setSelectedVariant(data.product.variants?.[0] || null);
      });
  }, [id]);

  if (!product) return <div className="product-loading">Loading...</div>;

  // Helper: Render average rating
  const renderRating = (rating) => (
    <span className="badge bg-warning text-dark">{rating ? `★ ${rating.toFixed(1)}` : 'No ratings yet'}</span>
  );

  // Helper: Render purchase controls
  const renderPurchaseControls = (price, onAdd) => (
    <div className="d-flex align-items-center gap-2 my-2">
      <label className="form-label mb-0">Qty:</label>
      <input
        type="number"
        min={1}
        className="form-control w-auto"
        style={{maxWidth: '80px'}}
        value={quantity}
        onChange={e => setQuantity(Math.max(1, Number(e.target.value)))}
      />
      <span className="fw-bold fs-5">${price}</span>
      <Button kind="primary" onClick={onAdd}>Add to cart</Button>
    </div>
  );

  // Simulate seller info (replace with real data as needed)
  const seller = product.seller || { name: 'Seller Name' };

  // Simulate reviews (replace with real data as needed)
  const reviews = product.reviews || [];

  // Add to cart handler: guest -> local storage; user -> backend API
  const handleAddToCart = async (prod, variant, qty) => {
    try {
      if (!user) {
        addGuestCartItem(prod, variant, qty);
      } else {
        // Minimal server-side add: use existing API if available
        if (typeof addToCartApi === 'function') {
          await addToCartApi({ product_id: prod?.id ?? prod?.product_id, quantity: qty, variant_id: variant?.id ?? variant?.variant_id });
        }
      }
      setToast({ open: true, kind: 'success', message: `Added ${qty} of ${prod.name}${variant ? ' (' + variant.name + ')' : ''} to cart.` });
    } catch (e) {
      setToast({ open: true, kind: 'error', message: 'Failed to add to cart.' });
    }
  };

  return (
    <>
      <div className="container py-4">
        <PageHeader title={product.name} subtitle={product.category ? `${product.category}${product.subcategory ? ' / ' + product.subcategory : ''}` : ''} />
        <div className="row g-4 align-items-center">
          <div className="col-md-6">
            <div className="mb-2 text-muted">{seller.name}</div>
            {renderRating(product.rating)}
            {(!product.variants || product.variants.length === 0) && renderPurchaseControls(product.price, () => handleAddToCart(product, null, quantity))}
            <div className="mt-3">{product.description}</div>
          </div>
          <div className="col-md-6 text-center">
            <img src={product.image_url} alt={product.name} className="img-fluid rounded shadow" style={{maxHeight: '350px'}} />
          </div>
        </div>

        {product.variants && product.variants.length > 0 && (
          <div className="mt-4">
            <div className="mb-2 fw-bold">Select Variant:</div>
            <div className="d-flex flex-wrap gap-2">
              <VariantsList
                variants={product.variants}
                selected={selectedVariant}
                onSelect={setSelectedVariant}
              />
            </div>
            {selectedVariant && renderPurchaseControls(selectedVariant.price ?? product.price, () => handleAddToCart(product, selectedVariant, quantity))}
          </div>
        )}

        <div className="mt-5">
          <h4>Reviews</h4>
          {reviews.length > 0 ? (
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
        <Toast open={toast.open} kind={toast.kind} message={toast.message} onClose={() => setToast({ ...toast, open: false })} />
      </div>
    </>
  );
};

const VariantsList = memo(({ variants, selected, onSelect }) => (
  <>
    {variants.map(variant => (
      <button
        key={variant.id ?? variant.variant_id}
        className={`btn btn-outline-secondary ${selected && (selected.id ?? selected.variant_id) === (variant.id ?? variant.variant_id) ? 'active' : ''}`}
        onClick={() => onSelect(variant)}
      >
        {variant.name ?? 'Variant'}
      </button>
    ))}
  </>
));

export default ProductDetailPage;
