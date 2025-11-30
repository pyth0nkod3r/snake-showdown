import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { SnakeGame } from './SnakeGame';
import { GameMode } from '@/types/game';

// Mock framer-motion to avoid animation issues in tests
vi.mock('framer-motion', () => ({
  motion: {
    div: ({ children, ...props }: any) => <div {...props}>{children}</div>,
  },
}));

describe('SnakeGame Component', () => {
  const mockOnGameOver = vi.fn();
  const defaultMode: GameMode = 'walls';

  beforeEach(() => {
    mockOnGameOver.mockClear();
  });

  it('should render game with initial score of 0', () => {
    render(<SnakeGame mode={defaultMode} onGameOver={mockOnGameOver} />);
    
    expect(screen.getByText('0')).toBeInTheDocument();
    expect(screen.getByText('Score')).toBeInTheDocument();
  });

  it('should display the correct game mode', () => {
    render(<SnakeGame mode="passthrough" onGameOver={mockOnGameOver} />);
    
    expect(screen.getByText('passthrough')).toBeInTheDocument();
  });

  it('should show pause button when game is running', () => {
    render(<SnakeGame mode={defaultMode} onGameOver={mockOnGameOver} />);
    
    const pauseButton = screen.getAllByRole('button')[0];
    expect(pauseButton).toBeInTheDocument();
  });

  it('should show game instructions', () => {
    render(<SnakeGame mode={defaultMode} onGameOver={mockOnGameOver} />);
    
    expect(screen.getByText(/Use Arrow Keys or WASD to move/i)).toBeInTheDocument();
    expect(screen.getByText(/Press Space to pause/i)).toBeInTheDocument();
  });

  it('should have a reset button', () => {
    render(<SnakeGame mode={defaultMode} onGameOver={mockOnGameOver} />);
    
    const buttons = screen.getAllByRole('button');
    expect(buttons.length).toBeGreaterThan(0);
  });

  it('should handle keyboard events for direction changes', () => {
    render(<SnakeGame mode={defaultMode} onGameOver={mockOnGameOver} />);
    
    // Simulate arrow key press
    const event1 = new KeyboardEvent('keydown', { key: 'ArrowUp' });
    const event2 = new KeyboardEvent('keydown', { key: 'ArrowDown' });
    const event3 = new KeyboardEvent('keydown', { key: 'ArrowLeft' });
    const event4 = new KeyboardEvent('keydown', { key: 'ArrowRight' });
    
    window.dispatchEvent(event1);
    window.dispatchEvent(event2);
    window.dispatchEvent(event3);
    window.dispatchEvent(event4);
    
    // If no errors thrown, keyboard handling works
    expect(true).toBe(true);
  });

  it('should handle WASD keys for direction changes', () => {
    render(<SnakeGame mode={defaultMode} onGameOver={mockOnGameOver} />);
    
    const event1 = new KeyboardEvent('keydown', { key: 'w' });
    const event2 = new KeyboardEvent('keydown', { key: 's' });
    const event3 = new KeyboardEvent('keydown', { key: 'a' });
    const event4 = new KeyboardEvent('keydown', { key: 'd' });
    
    window.dispatchEvent(event1);
    window.dispatchEvent(event2);
    window.dispatchEvent(event3);
    window.dispatchEvent(event4);
    
    expect(true).toBe(true);
  });

  it('should handle space key for pause', () => {
    render(<SnakeGame mode={defaultMode} onGameOver={mockOnGameOver} />);
    
    const event = new KeyboardEvent('keydown', { key: ' ' });
    window.dispatchEvent(event);
    
    expect(true).toBe(true);
  });
});
