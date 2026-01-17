import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import DecisionFrame from '../DecisionFrame';

describe('DecisionFrame', () => {
  test('returns null when not visible', () => {
    const { container } = render(<DecisionFrame visible={false} />);
    expect(container.firstChild).toBeNull();
  });

  test('renders banner, preview and triggers actions', async () => {
    const onConfirm = jest.fn();
    const onCancel = jest.fn();
    render(
      <DecisionFrame visible banner="Confirm Action" preview="Preview text" onConfirm={onConfirm} onCancel={onCancel}>
        <div>Body</div>
      </DecisionFrame>
    );
    expect(screen.getByText('Confirm Action')).toBeInTheDocument();
    expect(screen.getByText('Preview text')).toBeInTheDocument();
    await userEvent.click(screen.getByText('Confirm'));
    await userEvent.click(screen.getByText('Cancel'));
    expect(onConfirm).toHaveBeenCalledTimes(1);
    expect(onCancel).toHaveBeenCalledTimes(1);
  });
});
