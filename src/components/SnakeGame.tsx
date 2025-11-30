import { useEffect } from 'react';
import { useSnakeGame } from '@/hooks/useSnakeGame';
import { GameCanvas } from './GameCanvas';
import { Button } from './ui/button';
import { GameMode } from '@/types/game';
import { Play, Pause, RotateCcw } from 'lucide-react';
import { motion } from 'framer-motion';

interface SnakeGameProps {
  mode: GameMode;
  onGameOver: (score: number) => void;
}

export const SnakeGame = ({ mode, onGameOver }: SnakeGameProps) => {
  const { gameState, resetGame, togglePause, changeDirection } = useSnakeGame(mode);

  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (gameState.isGameOver) return;

      switch (e.key) {
        case 'ArrowUp':
        case 'w':
        case 'W':
          e.preventDefault();
          changeDirection('UP');
          break;
        case 'ArrowDown':
        case 's':
        case 'S':
          e.preventDefault();
          changeDirection('DOWN');
          break;
        case 'ArrowLeft':
        case 'a':
        case 'A':
          e.preventDefault();
          changeDirection('LEFT');
          break;
        case 'ArrowRight':
        case 'd':
        case 'D':
          e.preventDefault();
          changeDirection('RIGHT');
          break;
        case ' ':
          e.preventDefault();
          togglePause();
          break;
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [changeDirection, togglePause, gameState.isGameOver]);

  useEffect(() => {
    if (gameState.isGameOver) {
      onGameOver(gameState.score);
    }
  }, [gameState.isGameOver, gameState.score, onGameOver]);

  return (
    <div className="flex flex-col items-center gap-6">
      {/* Game info */}
      <div className="flex items-center gap-8">
        <motion.div 
          className="text-center"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="text-sm text-muted-foreground uppercase tracking-wider">Score</div>
          <div className="text-4xl font-bold text-primary neon-text">{gameState.score}</div>
        </motion.div>
        
        <motion.div 
          className="text-center"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <div className="text-sm text-muted-foreground uppercase tracking-wider">Mode</div>
          <div className="text-xl font-semibold text-secondary capitalize">{mode}</div>
        </motion.div>
      </div>

      {/* Game canvas */}
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        <GameCanvas gameState={gameState} />
      </motion.div>

      {/* Controls */}
      <motion.div 
        className="flex items-center gap-4"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
      >
        <Button
          onClick={togglePause}
          disabled={gameState.isGameOver}
          variant="outline"
          size="lg"
          className="neon-glow"
        >
          {gameState.isPaused ? <Play className="w-5 h-5" /> : <Pause className="w-5 h-5" />}
        </Button>
        
        <Button
          onClick={resetGame}
          variant="outline"
          size="lg"
          className="neon-glow"
        >
          <RotateCcw className="w-5 h-5" />
        </Button>
      </motion.div>

      {/* Instructions */}
      {!gameState.isGameOver && (
        <motion.div 
          className="text-center text-sm text-muted-foreground"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          <p>Use Arrow Keys or WASD to move</p>
          <p>Press Space to pause</p>
        </motion.div>
      )}

      {/* Game over overlay */}
      {gameState.isGameOver && (
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="absolute inset-0 flex items-center justify-center bg-background/80 backdrop-blur-sm"
        >
          <div className="text-center space-y-6">
            <h2 className="text-6xl font-bold text-destructive neon-text">GAME OVER</h2>
            <p className="text-3xl text-primary">Final Score: {gameState.score}</p>
            <Button onClick={resetGame} size="lg" className="neon-glow">
              Play Again
            </Button>
          </div>
        </motion.div>
      )}
    </div>
  );
};
