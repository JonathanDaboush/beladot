import fetchMock from 'jest-fetch-mock';
import {
  getOrders,
  getOrderDetails,
  createShipmentEvent,
  getShipments
} from './shipmentService';

beforeEach(() => {
  fetchMock.resetMocks();
  global.fetch = fetchMock;
});

test('getOrders success', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ result: [{ id: 1 }] })
    })
  );
  const result = await getOrders();
  expect(result).toEqual([{ id: 1 }]);
});

test('getOrderDetails success', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ result: { id: 1 } })
    })
  );
  const result = await getOrderDetails(1);
  expect(result).toEqual({ id: 1 });
});

test('createShipmentEvent success', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ success: true })
    })
  );
  await expect(createShipmentEvent(1, { event: 'shipped' })).resolves.toBeUndefined();
});

test('getShipments success', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ result: [{ id: 1 }] })
    })
  );
  const result = await getShipments();
  expect(result).toEqual([{ id: 1 }]);
});
