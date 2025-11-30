import { useEffect, useRef } from 'react';
import { GameState } from '@/types/game';

interface GameCanvasProps {
  gameState: GameState;
  gridSize?: number;
}

const CELL_SIZE = 16;

export const GameCanvas = ({ gameState, gridSize = 30 }: GameCanvasProps) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.fillStyle = 'hsl(220, 30%, 8%)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw grid
    ctx.strokeStyle = 'hsl(180, 50%, 15%)';
    ctx.lineWidth = 0.5;
    for (let i = 0; i <= gridSize; i++) {
      // Vertical lines
      ctx.beginPath();
      ctx.moveTo(i * CELL_SIZE, 0);
      ctx.lineTo(i * CELL_SIZE, gridSize * CELL_SIZE);
      ctx.stroke();
      
      // Horizontal lines
      ctx.beginPath();
      ctx.moveTo(0, i * CELL_SIZE);
      ctx.lineTo(gridSize * CELL_SIZE, i * CELL_SIZE);
      ctx.stroke();
    }

    // Draw food with glow
    ctx.shadowBlur = 15;
    ctx.shadowColor = 'hsl(0, 100%, 60%)';
    ctx.fillStyle = 'hsl(0, 100%, 60%)';
    ctx.fillRect(
      gameState.food.x * CELL_SIZE + 2,
      gameState.food.y * CELL_SIZE + 2,
      CELL_SIZE - 4,
      CELL_SIZE - 4
    );

    // Reset shadow
    ctx.shadowBlur = 0;

    // Draw snake body with glow
    ctx.shadowBlur = 10;
    ctx.shadowColor = 'hsl(90, 100%, 50%)';
    gameState.snake.body.forEach((segment, index) => {
      if (index === 0) {
        // Head - brighter
        ctx.fillStyle = 'hsl(90, 100%, 60%)';
      } else {
        // Body - gradient based on position
        const alpha = 1 - (index / gameState.snake.body.length) * 0.3;
        ctx.fillStyle = `hsla(90, 100%, 50%, ${alpha})`;
      }
      
      ctx.fillRect(
        segment.x * CELL_SIZE + 1,
        segment.y * CELL_SIZE + 1,
        CELL_SIZE - 2,
        CELL_SIZE - 2
      );
    });

    ctx.shadowBlur = 0;
  }, [gameState, gridSize]);

  return (
    <canvas
      ref={canvasRef}
      width={gridSize * CELL_SIZE}
      height={gridSize * CELL_SIZE}
      className="border-2 border-primary neon-glow rounded-sm"
    />
  );
};
