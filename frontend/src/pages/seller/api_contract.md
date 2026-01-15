# Seller Product API Contract (Frontend-First)

## 1. Seller Product List (GET /api/search_products_for_seller)
- **Request params:**
  - seller_id (required)
  - page (optional, default 1)
  - pageSize (optional, default 25)
  - keywords (optional)
  - category_id (optional)
  - subcategory_id (optional)
  - min_price (optional)
  - max_price (optional)
- **Response:**
  - Array of product items, each with:
    - product_id
    - name
    - image_url (main image)
    - price
    - category_id
    - category_name
    - subcategory_id
    - subcategory_name
    - is_available
    - (any other fields shown in user product list)
  - Pagination info: total, page, pageSize

## 2. Seller Product Detail (GET /api/get_product)
- **Request params:**
  - product_id (required)
- **Response:**
  - All fields shown on user product detail page, plus:
    - total_stock (sum of all variant stocks)
    - variants: [
        variant_id, name, price, stock, is_available, ...
      ]
    - comments: [
        comment_id, text, user, response, ...
      ]
    - (all other user-visible fields)

## 3. Add/Edit/Delete Product
- **POST /api/create_product**: Accepts only fields needed for creation (see user product create, plus is_available)
- **PUT /api/edit_product**: Accepts only fields needed for edit (see user product edit, plus is_available)
- **DELETE /api/delete_product**: Accepts product_id, does soft delete only

## 4. Add/Edit/Delete Variant
- **DELETE /api/remove_variant**: Accepts variant_id, does soft delete only

## 5. Respond to Comment
- **PUT /api/respond_to_comment**: Accepts comment_id, response_text

## 6. Analysis and Payouts
- **GET /api/analyze_orders_for_product**: Accepts only params needed for seller analysis page
- **GET /api/get_seller_payout**: Accepts seller_id, year, month

---

# Notes
- All product and variant fields returned must match the user product list/detail, except for the extra seller-only fields (e.g., total_stock, is_available, comments, etc.).
- No extra fields or endpoints should be exposed.
- All deletions are soft deletes.
- The backend must strictly follow this contract.
