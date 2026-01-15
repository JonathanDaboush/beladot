// Moved from src/seller
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './SellerProductDetail.css';

export default function SellerProductDetail() {
  const { productId } = useParams();
  const [product, setProduct] = useState(null);
  const [comments, setComments] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // TODO: Fetch product detail and comments by productId
    // setProduct(response.product)
    // setComments(response.comments)
  }, [productId]);

  const handleEdit = () => navigate(`/seller/products/${productId}/edit`);
  const handleSoftDelete = () => {
    // TODO: Call soft delete API
  };
  const handleVariantDelete = (variantId) => {
    // TODO: Call soft delete variant API
  };
  const handleCommentResponse = (commentId, response) => {
    // TODO: Call respond to comment API
  };

  if (!product) return <div>Loading...</div>;

  const totalStock = product.variants?.reduce((sum, v) => sum + (v.stock || 0), 0) || 0;

  return (
    <div className="seller-product-detail">
      <h2>{product.name}</h2>
      <img src={product.image_url} alt={product.name} />
      <p>{product.description}</p>
      <p>Price: ${product.price}</p>
      <p>Category: {product.category_name}</p>
      <p>Total Stock: {totalStock}</p>
      <button onClick={handleEdit}>Edit Product</button>
      <button onClick={handleSoftDelete}>Soft Delete Product</button>
      <h3>Variants</h3>
      <ul>
        {product.variants?.map(variant => (
          <li key={variant.variant_id}>
            {variant.name} (Stock: {variant.stock})
            <button onClick={() => handleVariantDelete(variant.variant_id)}>Soft Delete</button>
          </li>
        ))}
      </ul>
      <h3>User Comments</h3>
      <ul>
        {comments.map(comment => (
          <li key={comment.comment_id}>
            <p>{comment.text}</p>
            <input type="text" placeholder="Respond..." onBlur={e => handleCommentResponse(comment.comment_id, e.target.value)} />
          </li>
        ))}
      </ul>
    </div>
  );
}
