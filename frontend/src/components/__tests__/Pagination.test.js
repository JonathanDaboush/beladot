import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Pagination from '../Pagination';

test('renders buttons and handles clicks', () => {
  const onPageChange = jest.fn();
  const onPageSizeChange = jest.fn();
  render(
    <Pagination page={2} pageSize={25} total={75} onPageChange={onPageChange} onPageSizeChange={onPageSizeChange} />
  );
  expect(screen.getAllByRole('button').length).toBeGreaterThan(0);
  fireEvent.click(screen.getByText('Previous'));
  expect(onPageChange).toHaveBeenCalledWith(1);
  fireEvent.change(screen.getByDisplayValue('25'), { target: { value: '50' } });
  expect(onPageSizeChange).toHaveBeenCalledWith(50);
});
