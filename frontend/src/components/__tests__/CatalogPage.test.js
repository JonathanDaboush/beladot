import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import CatalogPage from '../CatalogPage';

describe('CatalogPage', () => {
  const items = Array.from({ length: 10 }, (_, i) => ({ id: i + 1, name: `Item ${i + 1}` }));
  const renderSummary = (item) => <div>{item.name}</div>;

  test('shows empty state when no items', () => {
    render(<CatalogPage items={[]} page={1} pageSize={5} onItemClick={() => {}} renderSummary={renderSummary} />);
    expect(screen.getByText('No items available')).toBeInTheDocument();
  });

  test('renders paged items and supports click', async () => {
    const onItemClick = jest.fn();
    render(<CatalogPage items={items} page={1} pageSize={5} onItemClick={onItemClick} renderSummary={renderSummary} />);
    expect(screen.getByText('Item 1')).toBeInTheDocument();
    await userEvent.click(screen.getByText('Item 1'));
    expect(onItemClick).toHaveBeenCalledWith(expect.objectContaining({ id: 1 }));
  });

  test('pagination next/prev buttons call onPageChange', async () => {
    const onPageChange = jest.fn();
    render(<CatalogPage items={items} page={1} pageSize={5} onItemClick={() => {}} renderSummary={renderSummary} onPageChange={onPageChange} />);
    await userEvent.click(screen.getByText('Next'));
    expect(onPageChange).toHaveBeenCalledWith(2);
  });
});
