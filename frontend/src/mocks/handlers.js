import { http } from 'msw';

export const handlers = [
  http.get('/api/finance/issues', (req, res, ctx) => {
    return res(ctx.json({ items: [{ id: 1, description: 'Test Issue', cost: 100, status: 'open' }] }));
  }),
  http.get('/api/finance/issues/:issueId', (req, res, ctx) => {
    return res(ctx.json({ item: { id: req.params.issueId, description: 'Test Issue Detail', cost: 100, status: 'open' } }));
  }),
  http.get('/api/finance/reimbursements', (req, res, ctx) => {
    return res(ctx.json({ items: [{ id: 1, employee_id: 1, amount: 50, status: 'pending' }] }));
  }),
  http.get('/api/finance/reimbursements/:reimbursementId', (req, res, ctx) => {
    return res(ctx.json({ item: { id: req.params.reimbursementId, employee_id: 1, amount: 50, status: 'pending' } }));
  }),
  http.post('/api/preview', (req, res, ctx) => {
    return res(ctx.json({ preview: { buyer: 'Refunded $50', seller: 'Credited', shipment_action_required: false } }));
  }),
  http.get('/api/employee_components', (req, res, ctx) => {
    return res(ctx.json({ result: [{ id: 1, img_url: 'test.png', description: 'Test Component' }] }));
  }),
  http.get('/api/employee_components/for_employee', (req, res, ctx) => {
    return res(ctx.json({ result: [{ id: 1, img_url: 'test.png', description: 'Test Component for Employee' }] }));
  }),
];
