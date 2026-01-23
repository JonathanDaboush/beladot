import React, { useMemo, useState } from 'react';
import CatalogPage from '../components/CatalogPage';
import DetailPage from '../components/DetailPage';
import InfoBox from '../components/InfoBox';
import Reviews from '../components/Reviews';
import OrderAddressForm from '../components/OrderAddressForm';

const sampleProducts = [
  {
    id: 1,
    name: 'Aurora Desk Lamp',
    category: 'Home',
    subcategory: 'Lighting',
    price: 49.99,
    rating: 4.4,
    image: 'https://picsum.photos/seed/lamp/640/360',
    description: 'Minimalist lamp with warm LED glow for cozy desks.',
    variants: [
      { id: 'lamp-std', name: 'Standard', price: 49.99, image: 'https://picsum.photos/seed/lampv1/320/180' },
      { id: 'lamp-pro', name: 'Pro', price: 64.99, image: 'https://picsum.photos/seed/lampv2/320/180' }
    ],
    reviews: [
      {
        review_id: 'r1',
        author_name: 'Jane D.',
        created_at: new Date().toISOString(),
        text: 'Nice warm light. Perfect for late night reading.',
        seller_response: {
          author_name: 'Bela Seller',
          created_at: new Date().toISOString(),
          text: 'Thanks for the kind words!'
        }
      }
    ]
  },
  {
    id: 2,
    name: 'Glacier Water Bottle',
    category: 'Outdoors',
    subcategory: 'Hydration',
    price: 24.5,
    rating: 4.8,
    image: 'https://picsum.photos/seed/bottle/640/360',
    description: 'Insulated stainless bottle keeps drinks cold for 24h.',
    variants: [
      { id: 'bottle-500', name: '500ml', price: 19.99, image: 'https://picsum.photos/seed/bv1/320/180' },
      { id: 'bottle-1l', name: '1L', price: 24.5, image: 'https://picsum.photos/seed/bv2/320/180' }
    ],
    reviews: []
  },
  {
    id: 3,
    name: 'Nimbus Backpack',
    category: 'Travel',
    subcategory: 'Bags',
    price: 79.0,
    rating: 4.2,
    image: 'https://picsum.photos/seed/backpack/640/360',
    description: 'Lightweight everyday backpack with padded laptop sleeve.',
    variants: [],
    reviews: []
  }
];

export default function UiShowcasePage() {
  const [catalogPage, setCatalogPage] = useState(1);
  const [selected, setSelected] = useState(null);
  const [addressPreview, setAddressPreview] = useState(null);

  const showcaseItems = useMemo(() => {
    // Duplicate sample products to show pagination/grid behavior
    return Array.from({ length: 36 }, (_, i) => {
      const base = sampleProducts[i % sampleProducts.length];
      return { ...base, id: i + 1, name: `${base.name} #${i + 1}` };
    });
  }, []);

  return (
    <div className="page">
      <div className="section">
        <h2 className="h4 mb-3">Catalog Grid</h2>
        <p className="muted">Paginated grid using cards with image, meta and price.</p>
        {!selected ? (
          <CatalogPage
            items={showcaseItems}
            page={catalogPage}
            pageSize={25}
            onPageChange={setCatalogPage}
            onItemClick={(item) => setSelected(item)}
            renderSummary={(product) => (
              <div className="card h-100 shadow-sm border-0">
                <img src={product.image} alt={product.name} className="product-image" />
                <div className="product-body">
                  <div className="product-title">{product.name}</div>
                  <div className="product-subcategory">{product.category} / {product.subcategory}</div>
                  <div className="product-price mt-1">${'{'}product.price{'}'}</div>
                </div>
              </div>
            )}
          />
        ) : (
          <DetailPage
            item={selected}
            images={[selected.image, ...(selected.variants?.map(v => v.image) || [])]}
            variants={selected.variants}
            selectedVariant={selected.variants?.[0]}
            onVariantChange={() => {}}
            reviews={selected.reviews}
            onBack={() => setSelected(null)}
          />
        )}
      </div>

      <div className="section">
        <h2 className="h4 mb-3">Info Boxes</h2>
        <div className="row g-3">
          <div className="col-md-4"><InfoBox title="Free Shipping" text="Orders over $50 ship free." /></div>
          <div className="col-md-4"><InfoBox title="30-Day Returns" text="No-questions-asked returns within 30 days." /></div>
          <div className="col-md-4"><InfoBox title="Secure Checkout" text="256-bit SSL and encrypted payments." /></div>
        </div>
      </div>

      <div className="section">
        <h2 className="h4 mb-3">Reviews</h2>
        <Reviews reviews={sampleProducts[0].reviews} />
      </div>

      <div className="section">
        <h2 className="h4 mb-3">Order Address Form</h2>
        <div className="row g-3">
          <div className="col-md-6">
            <OrderAddressForm onChange={setAddressPreview} />
          </div>
          <div className="col-md-6">
            <div className="card">
              <div className="card-body">
                <div className="muted mb-2">Live Preview</div>
                <pre style={{ margin: 0 }}>{JSON.stringify(addressPreview || {}, null, 2)}</pre>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
