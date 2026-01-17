import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Header from '../Header';
import InfoBox from '../InfoBox';
import { ErrorBoundary } from '../ErrorBoundary.jsx';

jest.mock('../../context/AuthContext', () => ({
  useAuth: () => ({ isEmployee: false, isSeller: false }),
}));

jest.mock('../../hooks/usePortalType', () => ({
  usePortalType: () => 'user',
}));

describe('Header', () => {
  beforeEach(() => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () =>
          Promise.resolve({
            categories: [
              { category_id: 1, name: 'Food', subcategories: [{ subcategory_id: 10, name: 'Fruits' }] },
              { category_id: 2, name: 'Tech', subcategories: [] },
            ],
          }),
      })
    );
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('renders logo and search', async () => {
    render(<Header />);
    expect(await screen.findByText(/Bela/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Search products/i)).toBeInTheDocument();
  });

  it('renders category buttons from API', async () => {
    render(<Header />);
    expect(await screen.findByText('Food')).toBeInTheDocument();
    expect(screen.getByText('Tech')).toBeInTheDocument();
  });

  it('shows subcategory dropdown on hover', async () => {
    render(<Header />);
    const foodBtn = await screen.findByText('Food');
    fireEvent.mouseEnter(foodBtn);
    expect(await screen.findByText('Fruits')).toBeInTheDocument();
  });

  it('does not show dropdown for categories without subcategories', async () => {
    render(<Header />);
    const techBtn = await screen.findByText('Tech');
    fireEvent.mouseEnter(techBtn);
    expect(screen.queryByText('Fruits')).not.toBeInTheDocument();
  });

  it('renders InfoBox with title and text', () => {
    render(<InfoBox title="Tips" text="Always check variants" />);
    expect(screen.getByText('Tips')).toBeInTheDocument();
    expect(screen.getByText('Always check variants')).toBeInTheDocument();
  });

  it('ErrorBoundary renders fallback on error', () => {
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    const ProblemChild = () => { throw new Error('Boom'); };
    render(
      <ErrorBoundary>
        <ProblemChild />
      </ErrorBoundary>
    );
    expect(screen.getByText(/Something went wrong/i)).toBeInTheDocument();
    expect(screen.getByText(/Boom/i)).toBeInTheDocument();
    consoleSpy.mockRestore();
  });
});
