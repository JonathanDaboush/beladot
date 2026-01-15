import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
// import SellerProductCard from '../components/SellerProductCard'; // If needed for variants
import './ProductDetailPage.css';

export default function ProductDetailPage() {
  const { productId } = useParams();
  const [product, setProduct] = useState(null);
  const [comments, setComments] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // TODO: Fetch product detail and comments by productId
    // setProduct(response.product)
    // setComments(response.comments)
  }, [productId]);

  if (!product) return <div>Loading...</div>;

  const totalStock = product.variants?.reduce((sum, v) => sum + (v.stock || 0), 0) || 0;

  return (
    <div className="product-detail">
      <h2>{product.name}</h2>
      <img src={product.image_url} alt={product.name} />
      <p>{product.description}</p>
      <p>Price: ${product.price}</p>
      <p>Category: {product.category_name}</p>
      <p>Total Stock: {totalStock}</p>
      <button onClick={() => navigate(`/products/${productId}/edit`)}>Edit Product</button>
      <h3>Variants</h3>
      <ul>
        {product.variants?.map(variant => (
          <li key={variant.variant_id}>
            {variant.name} (Stock: {variant.stock})
            {/* Add soft delete or edit buttons if needed */}
          </li>
        ))}
      </ul>
      <h3>User Comments</h3>
      <ul>
        {comments.map(comment => (
          <li key={comment.comment_id}>
            <p>{comment.text}</p>
            <input type="text" placeholder="Respond..." />
          </li>
        ))}
      </ul>
    </div>
  );
}
