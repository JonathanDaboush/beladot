import React from 'react';
import { render } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';

// Mock AuthContext at the top-level so it's hoisted correctly
jest.mock('../../context/AuthContext', () => ({
  __esModule: true,
  useAuth: () => ({ user: null })
}));

import ProductDetailPage from '../ProductDetailPage';

beforeEach(() => {
  jest.spyOn(global, 'fetch').mockImplementation((url) => {
    if (url === '/api/product/123') {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({
          product: {
            id: 123,
            name: 'Widget',
            category: 'Gadgets',
            subcategory: 'Widgets',
            image_url: '/img/widget.png',
            price: 10,
            variants: [],
            rating: 4.5,
            description: 'A great widget.'
          }
         })
       });
     }
     return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
  });
});

afterEach(() => {
  if (global.fetch.mockRestore) global.fetch.mockRestore();
});

describe('ProductDetailPage', () => {
  it('shows PageHeader with product name', async () => {
    const { findByText } = render(
      <MemoryRouter initialEntries={["/product/123"]}>
        <Routes>
          <Route path="/product/:id" element={<ProductDetailPage />} />
        </Routes>
      </MemoryRouter>
    );

    expect(await findByText('Widget')).toBeInTheDocument();
  });
});
