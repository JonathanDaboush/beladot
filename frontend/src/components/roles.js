export const ROLE_META = {
  user: {
    name: 'Customer',
    pillColor: 'var(--role-user-accent)',
    homePath: '/',
    description: 'Shop products and manage orders',
  },
  seller: {
    name: 'Seller',
    pillColor: 'var(--role-seller-accent)',
    homePath: '/seller',
    description: 'Manage products, orders, payouts',
  },
  employee: {
    name: 'Employee',
    pillColor: 'var(--role-employee-accent)',
    homePath: '/employee',
    description: 'Schedules, requests, finance tasks',
  },
  manager: {
    name: 'Manager',
    pillColor: 'var(--role-manager-accent)',
    homePath: '/employee',
    description: 'Team oversight, approvals, incidents',
  },
};
