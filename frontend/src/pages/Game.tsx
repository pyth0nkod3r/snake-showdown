import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { SnakeGame } from '@/components/SnakeGame';
import { GameInstructions } from '@/components/GameInstructions';
import { Button } from '@/components/ui/button';
import { GameMode } from '@/types/game';
import { mockApi } from '@/services/mockBackend';
import { useToast } from '@/hooks/use-toast';
import { ArrowLeft, Trophy } from 'lucide-react';

export default function Game() {
  const [searchParams] = useSearchParams();
  const mode = (searchParams.get('mode') || 'walls') as GameMode;
  const navigate = useNavigate();
  const { toast } = useToast();
  const [hasSubmittedScore, setHasSubmittedScore] = useState(false);

  const handleGameOver = async (score: number) => {
    if (!hasSubmittedScore && score > 0) {
      await mockApi.submitScore(score, mode);
      setHasSubmittedScore(true);
      
      toast({
        title: '🎮 Game Over!',
        description: `Your score of ${score} has been saved.`,
      });
    }
  };

  return (
    <div className="min-h-screen p-8 grid-pattern">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between mb-8"
        >
          <Button
            variant="outline"
            onClick={() => navigate('/')}
            className="neon-glow"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back
          </Button>

          <Button
            variant="outline"
            onClick={() => navigate('/leaderboard')}
            className="neon-glow-secondary"
          >
            <Trophy className="w-4 h-4 mr-2" />
            Leaderboard
          </Button>
        </motion.div>

        {/* Game and Instructions */}
        <div className="flex flex-col lg:flex-row gap-8 items-start justify-center">
          <SnakeGame mode={mode} onGameOver={handleGameOver} />
          <div className="w-full lg:w-80">
            <GameInstructions mode={mode} />
          </div>
        </div>
      </div>
    </div>
  );
}
