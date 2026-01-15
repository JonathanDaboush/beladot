
/**
 * useWishlistItems
 *
 * Custom React hook to fetch and manage wishlist items for the user.
 * Handles loading and error states, returns normalized wishlist data.
 *
 * Usage:
 *   const { data, loading, error } = useWishlistItems();
 */
import { useEffect, useState } from 'react';
import { fetchWishlistItems } from '../api/wishlist';

export default function useWishlistItems() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetchWishlistItems()
      .then(data => {
        // Normalize wishlist item data for UI consumption
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
        }));
        setData(items);
        setLoading(false);
      })
      .catch(e => {
        setError(e.message);
        setLoading(false);
      });
  }, []);

  // Return wishlist data, loading, and error states
  return { data, loading, error };
}
