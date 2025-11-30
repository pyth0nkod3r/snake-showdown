import { useState, useEffect, useCallback, useRef } from 'react';
import { GameState, Direction, Position, GameMode } from '@/types/game';

const GRID_SIZE = 30;
const INITIAL_SPEED = 150;
const SPEED_INCREMENT = 5;

export const useSnakeGame = (mode: GameMode) => {
  const [gameState, setGameState] = useState<GameState>(getInitialGameState(mode));
  const [gameSpeed, setGameSpeed] = useState(INITIAL_SPEED);
  const directionRef = useRef<Direction>('RIGHT');
  const lastDirectionRef = useRef<Direction>('RIGHT');

  function getInitialGameState(gameMode: GameMode): GameState {
    return {
      snake: {
        body: [
          { x: 15, y: 15 },
          { x: 14, y: 15 },
          { x: 13, y: 15 },
        ],
        direction: 'RIGHT',
      },
      food: generateFood([{ x: 15, y: 15 }]),
      score: 0,
      isGameOver: false,
      isPaused: false,
      mode: gameMode,
    };
  }

  const resetGame = useCallback(() => {
    setGameState(getInitialGameState(mode));
    setGameSpeed(INITIAL_SPEED);
    directionRef.current = 'RIGHT';
    lastDirectionRef.current = 'RIGHT';
  }, [mode]);

  const togglePause = useCallback(() => {
    setGameState(prev => ({ ...prev, isPaused: !prev.isPaused }));
  }, []);

  const changeDirection = useCallback((newDirection: Direction) => {
    const opposite = {
      UP: 'DOWN',
      DOWN: 'UP',
      LEFT: 'RIGHT',
      RIGHT: 'LEFT',
    };

    // Prevent 180-degree turns
    if (opposite[newDirection] !== lastDirectionRef.current) {
      directionRef.current = newDirection;
    }
  }, []);

  useEffect(() => {
    if (gameState.isGameOver || gameState.isPaused) return;

    const gameLoop = setInterval(() => {
      setGameState(prevState => {
        const newHead = getNextHead(prevState.snake.body[0], directionRef.current);
        lastDirectionRef.current = directionRef.current;

        // Check wall collision for walls mode
        if (mode === 'walls') {
          if (
            newHead.x < 0 ||
            newHead.x >= GRID_SIZE ||
            newHead.y < 0 ||
            newHead.y >= GRID_SIZE
          ) {
            return { ...prevState, isGameOver: true };
          }
        } else {
          // Pass-through mode - wrap around
          newHead.x = (newHead.x + GRID_SIZE) % GRID_SIZE;
          newHead.y = (newHead.y + GRID_SIZE) % GRID_SIZE;
        }

        // Check self collision
        if (checkCollision(newHead, prevState.snake.body)) {
          return { ...prevState, isGameOver: true };
        }

        const newBody = [newHead, ...prevState.snake.body];

        // Check food collision
        if (newHead.x === prevState.food.x && newHead.y === prevState.food.y) {
          const newScore = prevState.score + 10;
          
          // Increase speed every 50 points
          if (newScore % 50 === 0) {
            setGameSpeed(prev => Math.max(50, prev - SPEED_INCREMENT));
          }

          return {
            ...prevState,
            snake: {
              ...prevState.snake,
              body: newBody,
            },
            food: generateFood(newBody),
            score: newScore,
          };
        }

        // Remove tail if no food eaten
        newBody.pop();

        return {
          ...prevState,
          snake: {
            ...prevState.snake,
            body: newBody,
          },
        };
      });
    }, gameSpeed);

    return () => clearInterval(gameLoop);
  }, [gameState.isGameOver, gameState.isPaused, gameSpeed, mode]);

  return {
    gameState,
    resetGame,
    togglePause,
    changeDirection,
  };
};

function getNextHead(head: Position, direction: Direction): Position {
  const moves = {
    UP: { x: 0, y: -1 },
    DOWN: { x: 0, y: 1 },
    LEFT: { x: -1, y: 0 },
    RIGHT: { x: 1, y: 0 },
  };

  const move = moves[direction];
  return {
    x: head.x + move.x,
    y: head.y + move.y,
  };
}

function checkCollision(head: Position, body: Position[]): boolean {
  return body.some(segment => segment.x === head.x && segment.y === head.y);
}

function generateFood(snakeBody: Position[]): Position {
  let food: Position;
  do {
    food = {
      x: Math.floor(Math.random() * GRID_SIZE),
      y: Math.floor(Math.random() * GRID_SIZE),
    };
  } while (snakeBody.some(segment => segment.x === food.x && segment.y === food.y));
  
  return food;
}

// Export for testing
export const gameUtils = {
  getNextHead,
  checkCollision,
  generateFood,
  GRID_SIZE,
};
