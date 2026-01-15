import fetchMock from 'jest-fetch-mock';
import {
  fetchIssues,
  fetchIssueDetail,
  fetchReimbursements,
  fetchReimbursementDetail
} from './financeService';

beforeEach(() => {
  fetchMock.resetMocks();
  global.fetch = fetchMock;
});

test('fetchIssues success', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ items: [{ id: 1 }] })
    })
  );
  const result = await fetchIssues();
  expect(result).toEqual({ items: [{ id: 1 }] });
});

test('fetchIssues failure', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: false,
      status: 500,
      json: () => Promise.resolve({})
    })
  );
  await expect(fetchIssues()).rejects.toThrow('Failed to fetch issues');
});

test('fetchIssueDetail success', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ id: 1 })
    })
  );
  const result = await fetchIssueDetail(1);
  expect(result).toEqual({ id: 1 });
});

test('fetchIssueDetail failure', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: false,
      status: 404,
      json: () => Promise.resolve({})
    })
  );
  await expect(fetchIssueDetail(999)).rejects.toThrow('Failed to fetch issue detail');
});

test('fetchReimbursements success', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ items: [{ id: 1 }] })
    })
  );
  const result = await fetchReimbursements();
  expect(result).toEqual({ items: [{ id: 1 }] });
});

test('fetchReimbursements failure', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: false,
      status: 500,
      json: () => Promise.resolve({})
    })
  );
  await expect(fetchReimbursements()).rejects.toThrow('Failed to fetch reimbursements');
});

test('fetchReimbursementDetail success', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ id: 1 })
    })
  );
  const result = await fetchReimbursementDetail(1);
  expect(result).toEqual({ id: 1 });
});

test('fetchReimbursementDetail failure', async () => {
  fetchMock.mockImplementationOnce(() =>
    Promise.resolve({
      ok: false,
      status: 404,
      json: () => Promise.resolve({})
    })
  );
  await expect(fetchReimbursementDetail(999)).rejects.toThrow('Failed to fetch reimbursement detail');
});
