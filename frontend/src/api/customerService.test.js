import fetchMock from 'jest-fetch-mock';
import {
  getAllCustomerRefundRequests,
  getSpecificRefundRequest,
  approveOrDenyRefund,
  getShipmentGrievanceReports
} from './customerService';

beforeEach(() => {
  fetchMock.resetMocks();
  global.fetch = fetchMock;
});

test('getAllCustomerRefundRequests success', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ result: [{ id: 1 }] })
    })
  );
  const result = await getAllCustomerRefundRequests();
  expect(result).toEqual([{ id: 1 }]);
});

test('getAllCustomerRefundRequests empty', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ result: [] })
    })
  );
  const result = await getAllCustomerRefundRequests();
  expect(result).toEqual([]);
});

test('getSpecificRefundRequest success', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ result: { id: 1 } })
    })
  );
  const result = await getSpecificRefundRequest(1);
  expect(result).toEqual({ id: 1 });
});

test('getSpecificRefundRequest failure', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: false,
      status: 404,
      json: () => Promise.resolve({})
    })
  );
  const result = await getSpecificRefundRequest(999);
  expect(result).toBeUndefined();
});

test('approveOrDenyRefund success', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ success: true })
    })
  );
  await expect(approveOrDenyRefund(1, 'approve', 10, 'desc')).resolves.toBeUndefined();
});

test('getShipmentGrievanceReports success', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ result: [{ id: 1 }] })
    })
  );
  const result = await getShipmentGrievanceReports();
  expect(result).toEqual([{ id: 1 }]);
});
