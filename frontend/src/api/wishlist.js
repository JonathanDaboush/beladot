/**
 * Wishlist API
 *
 * Provides functions for interacting with wishlist endpoints.
 * All functions throw errors if requests fail.
 */

/**
 * Fetches all wishlist items for the current user.
 * @returns {Promise<Array>} List of wishlist items
 */
export async function fetchWishlistItems() {
  const res = await fetch('/api/wishlist');
  if (!res.ok) throw new Error('Failed to fetch wishlist items');
  return res.json();
}

/**
 * Edits the quantity of a specific wishlist item.
 * @param {string|number} itemId
 * @param {number} newQty
 * @returns {Promise<object>} Updated wishlist item
 */
export async function editWishlistItemQuantity(itemId, newQty) {
  const res = await fetch(`/api/wishlist/item/${itemId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ quantity: newQty })
  });
  if (!res.ok) throw new Error('Failed to update wishlist item');
  return res.json();
}

/**
 * Removes a wishlist item by ID.
 * @param {string|number} itemId
 * @returns {Promise<object>} Result of removal
 */
export async function removeWishlistItem(itemId) {
  const res = await fetch(`/api/wishlist/item/${itemId}`, {
    method: 'DELETE'
  });
  if (!res.ok) throw new Error('Failed to remove wishlist item');
  return res.json();
}
