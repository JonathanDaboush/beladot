import React from 'react';
import { render, screen } from '@testing-library/react';
import InfoBox from '../InfoBox';

describe('InfoBox', () => {
  test('renders title and text', () => {
    render(<InfoBox title="Hello" text="World" />);
    expect(screen.getByText('Hello')).toBeInTheDocument();
    expect(screen.getByText('World')).toBeInTheDocument();
    expect(screen.getByText('Hello').className).toContain('info-box-title');
    expect(screen.getByText('World').className).toContain('info-box-text');
  });

  test('handles empty props gracefully', () => {
    const { container } = render(<InfoBox title="" text="" />);
    // Container renders even with empty text
    expect(container.querySelector('.info-box')).toBeInTheDocument();
  });
});
