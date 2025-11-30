import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Game from './Game';

// Mock dependencies
vi.mock('@/components/SnakeGame', () => ({
  SnakeGame: ({ mode, onGameOver }: any) => (
    <div data-testid="snake-game">
      <div>Mode: {mode}</div>
      <button onClick={() => onGameOver(100)}>Trigger Game Over</button>
    </div>
  ),
}));

vi.mock('@/components/GameInstructions', () => ({
  GameInstructions: ({ mode }: any) => (
    <div data-testid="game-instructions">Instructions for {mode}</div>
  ),
}));

vi.mock('@/services/mockBackend', () => ({
  mockApi: {
    submitScore: vi.fn().mockResolvedValue(undefined),
  },
}));

vi.mock('framer-motion', () => ({
  motion: {
    div: ({ children, ...props }: any) => <div {...props}>{children}</div>,
  },
}));

const renderWithRouter = (initialRoute = '/game?mode=walls') => {
  window.history.pushState({}, '', initialRoute);
  return render(
    <BrowserRouter>
      <Game />
    </BrowserRouter>
  );
};

describe('Game Page', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render the game page', () => {
    renderWithRouter();
    
    expect(screen.getByTestId('snake-game')).toBeInTheDocument();
    expect(screen.getByTestId('game-instructions')).toBeInTheDocument();
  });

  it('should display back button', () => {
    renderWithRouter();
    
    expect(screen.getByText('Back')).toBeInTheDocument();
  });

  it('should display leaderboard button', () => {
    renderWithRouter();
    
    expect(screen.getByText('Leaderboard')).toBeInTheDocument();
  });

  it('should pass correct mode to SnakeGame component', () => {
    renderWithRouter('/game?mode=passthrough');
    
    expect(screen.getByText('Mode: passthrough')).toBeInTheDocument();
  });

  it('should default to walls mode if no mode specified', () => {
    renderWithRouter('/game');
    
    expect(screen.getByText('Mode: walls')).toBeInTheDocument();
  });

  it('should pass game mode to instructions component', () => {
    renderWithRouter('/game?mode=passthrough');
    
    expect(screen.getByText('Instructions for passthrough')).toBeInTheDocument();
  });
});
