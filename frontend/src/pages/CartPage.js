import React, { useEffect, useState, memo, useMemo } from 'react';
// ...existing code...
import { fetchCartItems, editCartItemQuantity, removeCartItem } from '../api/cart';

const CartPage = () => {
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadCart() {
      setLoading(true);
      setError(null);
      try {
        const data = await fetchCartItems();
        // Map backend data to frontend structure
        const items = (data.items || []).map((item) => ({
          id: item.variant_id || item.product_id,
          product: {
            name: item.product_name,
            image_url: item.product_image,
            category: item.category,
            subcategory: item.subcategory,
          },
          variant: item.variant_id ? {
            name: item.variant_name,
            image_url: item.variant_image,
          } : null,
          quantity: item.quantity,
          price: item.price,
          total: item.price * item.quantity,
        }));
        setCartItems(items);
      } catch (e) {
        setError(e.message);
      }
      setLoading(false);
    }
    loadCart();
  }, []);

        const cartTotal = useMemo(() => cartItems.reduce((sum, item) => sum + item.total, 0), [cartItems]);
    try {
      await editCartItemQuantity(itemId, newQty);
      // Refresh cart
      const data = await fetchCartItems();
      const items = (data.items || []).map((item) => ({
        id: item.variant_id || item.product_id,
        product: {
          name: item.product_name,
          image_url: item.product_image,
          category: item.category,
          subcategory: item.subcategory,
        },
        variant: item.variant_id ? {
          name: item.variant_name,
          image_url: item.variant_image,
                  <CartItemsList items={cartItems} />
      setError(e.message);
    }
  };

  const cartTotal = cartItems.reduce((sum, item) => sum + item.total, 0);

  return (
      );
    <div className="container py-4">
      const CartItemsList = memo(({ items }) => (
        <>
          {items.map(item => (
            <div className="col-md-6 col-lg-4" key={item.id}>
              <div className="card h-100">
                <div className="row g-0 align-items-center">
                  <div className="col-4">
                    <img
                      src={item.variant?.image_url || item.product.image_url}
                      alt={item.variant?.name || item.product.name}
                      className="img-fluid rounded-start"
                    />
                  </div>
                  <div className="col-8">
                    <div className="card-body">
                      <h5 className="card-title mb-1">{item.product.name}</h5>
                      <div className="text-muted small mb-1">
                        {item.product.category} / <span>{item.product.subcategory}</span>
                      </div>
                      {item.variant && (
                        <div className="mb-1"><span className="badge bg-info text-dark">Variant: {item.variant.name}</span></div>
                      )}
                      <div className="mb-1">
                        Qty: <span className="fw-bold">{item.quantity}</span>
                        <button className="btn btn-sm btn-outline-primary ms-2" onClick={() => handleEditQuantity(item.id, item.quantity + 1)}>+</button>
                        <button className="btn btn-sm btn-outline-primary ms-1" onClick={() => handleEditQuantity(item.id, Math.max(1, item.quantity - 1))}>-</button>
                      </div>
                      <div className="mb-1">Price: <span className="fw-bold">${item.price}</span></div>
                      <div className="mb-1">Total: <span className="fw-bold">${item.total}</span></div>
                      <button className="btn btn-sm btn-outline-danger mt-2" onClick={() => handleRemove(item.id)}>Remove</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </>
      ));
      <h2 className="mb-4">Your Cart</h2>
      {loading ? (
        <div className="alert alert-info">Loading...</div>
      ) : error ? (
        <div className="alert alert-danger">{error}</div>
      ) : (
        <div className="row g-3">
          {cartItems.length === 0 ? (
            <div className="col-12">
              <div className="alert alert-secondary text-center">Your cart is empty.</div>
            </div>
          ) : (
            cartItems.map(item => (
              <div className="col-md-6 col-lg-4" key={item.id}>
                <div className="card h-100">
                  <div className="row g-0 align-items-center">
                    <div className="col-4">
                      <img
                        src={item.variant?.image_url || item.product.image_url}
                        alt={item.variant?.name || item.product.name}
                        className="img-fluid rounded-start"
                      />
                    </div>
                    <div className="col-8">
                      <div className="card-body">
                        <h5 className="card-title mb-1">{item.product.name}</h5>
                        <div className="text-muted small mb-1">
                          {item.product.category} / <span>{item.product.subcategory}</span>
                        </div>
                        {item.variant && (
                          <div className="mb-1"><span className="badge bg-info text-dark">Variant: {item.variant.name}</span></div>
                        )}
                        <div className="mb-1">
                          Qty: <span className="fw-bold">{item.quantity}</span>
                          <button className="btn btn-sm btn-outline-primary ms-2" onClick={() => handleEditQuantity(item.id, item.quantity + 1)}>+</button>
                          <button className="btn btn-sm btn-outline-primary ms-1" onClick={() => handleEditQuantity(item.id, Math.max(1, item.quantity - 1))}>-</button>
                        </div>
                        <div className="mb-1">Price: <span className="fw-bold">${item.price}</span></div>
                        <div className="mb-1">Total: <span className="fw-bold">${item.total}</span></div>
                        <button className="btn btn-sm btn-outline-danger mt-2" onClick={() => handleRemove(item.id)}>Remove</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      )}
      <div className="mt-4 text-end">
        <h4>Total: <span className="fw-bold">${cartTotal}</span></h4>
      </div>
    </div>
                  <div className="cart-item-category">
                    {item.product.category} / <span className="cart-item-subcategory">{item.product.subcategory}</span>
                  </div>
                  {item.variant && (
                    <div className="cart-item-variant">Variant: {item.variant.name}</div>
                  )}
                  <div className="cart-item-qty">
                    Qty: <input
                      type="number"
                      min={1}
                      value={item.quantity}
                      onChange={e => handleEditQuantity(item.id, Number(e.target.value))}
                    />
                  </div>
                  <div className="cart-item-price">Price: ${item.price}</div>
                  <div className="cart-item-total">Total: ${item.total}</div>
                  <button className="cart-remove-btn" onClick={() => handleRemove(item.id)}>Remove</button>
                </div>
              </div>
            ))
          )}
        </div>
      )}
      <div className="cart-total-row">
        <span>Cart Total:</span>
        <span className="cart-total">${cartTotal}</span>
      </div>
    </div>
  );
};

export default CartPage;
