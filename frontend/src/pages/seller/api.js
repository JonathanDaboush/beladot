// Moved from src/seller
const API_BASE = '/api';

export async function fetchSellerProducts({ keywords, category_id, subcategory_id, min_price, max_price, page, pageSize }) {
  const params = new URLSearchParams({
    keywords,
    category_id,
    subcategory_id,
    min_price,
    max_price,
    page,
    pageSize
  });
  const res = await fetch(`${API_BASE}/search_products_for_seller?${params}`);
  if (res.status === 401 || res.status === 403) throw new Error('Unauthorized or forbidden');
  const data = await res.json();
  return data.result || [];
}

export async function fetchSellerProductDetail(product_id) {
  const params = new URLSearchParams({ product_id });
  const res = await fetch(`${API_BASE}/get_product?${params}`);
  const data = await res.json();
  return data.result;
}

export async function createSellerProduct(productData) {
  const res = await fetch(`${API_BASE}/create_product`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(productData)
  });
  const data = await res.json();
  return data.result;
}

export async function editSellerProduct(productData) {
  const res = await fetch(`${API_BASE}/edit_product`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(productData)
  });
  const data = await res.json();
  return data.result;
}

export async function softDeleteSellerProduct(product_id) {
  const res = await fetch(`${API_BASE}/delete_product`, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_id })
  });
  const data = await res.json();
  return data.result;
}

export async function softDeleteVariant(variant_id) {
  const res = await fetch(`${API_BASE}/remove_variant`, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ variant_id })
  });
  const data = await res.json();
  return data.result;
}

export async function respondToComment(comment_id, response_text, db) {
  const res = await fetch(`${API_BASE}/respond_to_comment`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ comment_id, response_text, db })
  });
  const data = await res.json();
  return data.result;
}

export async function fetchSellerAnalysis(params) {
  const search = new URLSearchParams(params);
  const res = await fetch(`${API_BASE}/analyze_orders_for_product?${search}`);
  const data = await res.json();
  return data.result;
}

export async function fetchSellerPayouts({ year, month, db }) {
  const params = new URLSearchParams({ year, month, db });
  const res = await fetch(`${API_BASE}/get_seller_payout?${params}`);
  if (res.status === 401 || res.status === 403) throw new Error('Unauthorized or forbidden');
  const data = await res.json();
  return data.result;
}
