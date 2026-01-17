import React, { useState, memo } from 'react';
// ...existing code...
import { editWishlistItemQuantity, removeWishlistItem } from '../api/wishlist';
import DecisionFrame from '../components/DecisionFrame';
import useWishlistItems from '../hooks/useWishlistItems';


const WishlistPage = () => {
  const { data: wishlistItems, loading, error } = useWishlistItems();
  const [decisionMode, setDecisionMode] = useState(false);
  const [decisionType, setDecisionType] = useState('');
  const [selectedItem, setSelectedItem] = useState(null);
  const [newQty, setNewQty] = useState(1);
  const [preview, setPreview] = useState('');

  // Backend-powered preview (simulate for now)
  const getPreview = async (type, item, qty) => {
    if (type === 'edit') {
      return `Change quantity of ${item.product.name}${item.variant ? ' (' + item.variant.name + ')' : ''} to ${qty}`;
    } else if (type === 'remove') {
      return `Remove ${item.product.name}${item.variant ? ' (' + item.variant.name + ')' : ''} from wishlist.`;
    }
    return '';
  };

  const openDecision = async (type, item) => {
    setDecisionType(type);
    setSelectedItem(item);
    setNewQty(item.quantity);
    setPreview(await getPreview(type, item, item.quantity));
    setDecisionMode(true);
  };

    const WishlistItemsList = memo(({ items, onEdit, onRemove }) => (
      <>
        {items.map(item => (
          <div key={item.id} className="wishlist-item">
            {/* ...existing item rendering... */}
          </div>
        ))}
      </>
    ));
  const handleConfirm = async () => {
    try {
      if (decisionType === 'edit') {
        await editWishlistItemQuantity(selectedItem.id, newQty);
      } else if (decisionType === 'remove') {
        await removeWishlistItem(selectedItem.id);
      }
      // Optionally: trigger a reload via a context or state update if needed
      setDecisionMode(false);
      setSelectedItem(null);
      setPreview('');
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <div className="container py-4">
      <h2 className="mb-4">Your Wishlist</h2>
      {loading ? (
        <div className="alert alert-info">Loading...</div>
      ) : error ? (
        <div className="alert alert-danger">{error}</div>
      ) : (
        <div className="row g-3">
          {wishlistItems.length === 0 ? (
            <div className="col-12">
              <div className="alert alert-secondary text-center">Your wishlist is empty.</div>
            </div>
          ) : (
            wishlistItems.map(item => (
              <div className="col-md-6 col-lg-4" key={item.id}>
                <div className="card h-100">
                  <div className="row g-0 align-items-center">
                    <div className="col-4">
                      <img
                        src={item.variant?.image_url || item.product.image_url}
                        alt={item.variant?.name || item.product.name}
                        className="img-fluid rounded-start"
                      />
        {decisionType === 'edit' && selectedItem && (
          <div>
            <div className="mb-2">Edit quantity for <b>{selectedItem.product.name}{selectedItem.variant ? ' (' + selectedItem.variant.name + ')' : ''}</b></div>
            <input
              type="number"
              min={1}
              className="form-control w-50"
              value={newQty}
              onChange={async e => {
                setNewQty(Number(e.target.value));
                setPreview(await getPreview('edit', selectedItem, Number(e.target.value)));
              }}
            />
          </div>
        )}
        {decisionType === 'remove' && selectedItem && (
          <div>Are you sure you want to remove <b>{selectedItem.product.name}{selectedItem.variant ? ' (' + selectedItem.variant.name + ')' : ''}</b> from your wishlist?</div>
        )}
      </DecisionFrame>
    </div>
  );
};

export default WishlistPage;
