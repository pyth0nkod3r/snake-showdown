import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { GameInstructions } from './GameInstructions';

// Mock framer-motion
vi.mock('framer-motion', () => ({
  motion: {
    div: ({ children, ...props }: any) => <div {...props}>{children}</div>,
  },
}));

describe('GameInstructions Component', () => {
  it('should render walls mode instructions', () => {
    render(<GameInstructions mode="walls" />);
    
    expect(screen.getByText('Walls Mode')).toBeInTheDocument();
    expect(screen.getByText('Classic snake with boundaries')).toBeInTheDocument();
    expect(screen.getByText(/Hitting the walls ends the game/i)).toBeInTheDocument();
  });

  it('should render pass-through mode instructions', () => {
    render(<GameInstructions mode="passthrough" />);
    
    expect(screen.getByText('Pass-Through Mode')).toBeInTheDocument();
    expect(screen.getByText('Snake wraps around the screen')).toBeInTheDocument();
    expect(screen.getByText(/Pass through edges to appear on the opposite side/i)).toBeInTheDocument();
  });

  it('should display controls section', () => {
    render(<GameInstructions mode="walls" />);
    
    expect(screen.getByText('Controls:')).toBeInTheDocument();
    expect(screen.getByText(/Arrow Keys or WASD - Move/i)).toBeInTheDocument();
    expect(screen.getByText(/Space - Pause\/Resume/i)).toBeInTheDocument();
  });

  it('should display rules section for walls mode', () => {
    render(<GameInstructions mode="walls" />);
    
    expect(screen.getByText('Rules:')).toBeInTheDocument();
    expect(screen.getByText(/Avoid running into yourself/i)).toBeInTheDocument();
    expect(screen.getByText(/Speed increases every 50 points/i)).toBeInTheDocument();
  });

  it('should display rules section for pass-through mode', () => {
    render(<GameInstructions mode="passthrough" />);
    
    expect(screen.getByText('Rules:')).toBeInTheDocument();
    expect(screen.getByText(/Only avoid running into yourself/i)).toBeInTheDocument();
    expect(screen.getByText(/Collect food to grow and score/i)).toBeInTheDocument();
  });

  it('should show different content for different modes', () => {
    const { rerender } = render(<GameInstructions mode="walls" />);
    const wallsText = screen.getByText(/Hitting the walls ends the game/i);
    expect(wallsText).toBeInTheDocument();
    
    rerender(<GameInstructions mode="passthrough" />);
    expect(screen.queryByText(/Hitting the walls ends the game/i)).not.toBeInTheDocument();
    expect(screen.getByText(/Pass through edges/i)).toBeInTheDocument();
  });
});
