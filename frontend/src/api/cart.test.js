import fetchMock from 'jest-fetch-mock';
import { fetchCartItems, editCartItemQuantity, removeCartItem } from './cart';

beforeEach(() => {
  fetchMock.resetMocks();
  global.fetch = fetchMock;
});

test('fetchCartItems success', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve([{ id: 1, name: 'item' }])
    })
  );
  const items = await fetchCartItems();
  expect(items).toEqual([{ id: 1, name: 'item' }]);
});

test('fetchCartItems failure', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: false,
      status: 500,
      json: () => Promise.resolve({})
    })
  );
  await expect(fetchCartItems()).rejects.toThrow('Failed to fetch cart items');
});

test('editCartItemQuantity success', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ id: 1, quantity: 2 })
    })
  );
  const result = await editCartItemQuantity(1, 2);
  expect(result).toEqual({ id: 1, quantity: 2 });
});

test('editCartItemQuantity failure', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: false,
      status: 400,
      json: () => Promise.resolve({})
    })
  );
  await expect(editCartItemQuantity(1, 2)).rejects.toThrow('Failed to update cart item');
});

test('removeCartItem success', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ success: true })
    })
  );
  const result = await removeCartItem(1);
  expect(result).toEqual({ success: true });
});

test('removeCartItem failure', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: false,
      status: 404,
      json: () => Promise.resolve({})
    })
  );
  await expect(removeCartItem(1)).rejects.toThrow('Failed to remove cart item');
});
