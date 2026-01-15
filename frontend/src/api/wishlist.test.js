import fetchMock from 'jest-fetch-mock';
import { fetchWishlistItems, editWishlistItemQuantity, removeWishlistItem } from './wishlist';

beforeEach(() => {
  fetchMock.resetMocks();
  global.fetch = fetchMock;
});

test('fetchWishlistItems success', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve([{ id: 1, name: 'item' }])
    })
  );
  const items = await fetchWishlistItems();
  expect(items).toEqual([{ id: 1, name: 'item' }]);
});

test('fetchWishlistItems failure', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: false,
      status: 500,
      json: () => Promise.resolve({})
    })
  );
  await expect(fetchWishlistItems()).rejects.toThrow('Failed to fetch wishlist items');
});

test('editWishlistItemQuantity success', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ id: 1, quantity: 2 })
    })
  );
  const result = await editWishlistItemQuantity(1, 2);
  expect(result).toEqual({ id: 1, quantity: 2 });
});

test('editWishlistItemQuantity failure', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: false,
      status: 400,
      json: () => Promise.resolve({})
    })
  );
  await expect(editWishlistItemQuantity(1, 2)).rejects.toThrow('Failed to update wishlist item');
});

test('removeWishlistItem success', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ success: true })
    })
  );
  const result = await removeWishlistItem(1);
  expect(result).toEqual({ success: true });
});

test('removeWishlistItem failure', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: false,
      status: 404,
      json: () => Promise.resolve({})
    })
  );
  await expect(removeWishlistItem(1)).rejects.toThrow('Failed to remove wishlist item');
});
