import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { GameCanvas } from '@/components/GameCanvas';
import { mockApi } from '@/services/mockBackend';
import { LiveGame } from '@/types/game';
import { ArrowLeft, Eye, Zap } from 'lucide-react';

export default function Spectate() {
  const navigate = useNavigate();
  const [liveGames, setLiveGames] = useState<LiveGame[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadLiveGames = async () => {
      const games = await mockApi.getLiveGames();
      setLiveGames(games);
      setIsLoading(false);
    };

    loadLiveGames();

    // Simulate live updates every 3 seconds
    const interval = setInterval(async () => {
      const games = await mockApi.getLiveGames();
      setLiveGames(games);
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen p-8 grid-pattern">
      <div className="max-w-7xl mx-auto">
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

          <div className="flex items-center gap-2">
            <Eye className="w-6 h-6 text-primary" />
            <h1 className="text-4xl font-bold text-primary neon-text">LIVE GAMES</h1>
          </div>
          
          <div className="flex items-center gap-2 text-accent">
            <Zap className="w-4 h-4 animate-pulse" />
            <span className="text-sm">LIVE</span>
          </div>
        </motion.div>

        {/* Live games grid */}
        {isLoading ? (
          <div className="text-center py-12">
            <div className="text-muted-foreground">Loading live games...</div>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
            {liveGames.map((game, index) => (
              <motion.div
                key={game.id}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="p-4 border-primary/20 neon-glow bg-card/50 backdrop-blur">
                  {/* Player info */}
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <div className="font-bold text-foreground">{game.player.username}</div>
                      <div className="text-xs text-muted-foreground capitalize">
                        {game.gameState.mode} mode
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-primary">
                        {game.gameState.score}
                      </div>
                      <div className="text-xs text-muted-foreground">score</div>
                    </div>
                  </div>

                  {/* Game canvas - smaller version */}
                  <div className="flex justify-center transform scale-75 origin-center -my-8">
                    <GameCanvas gameState={game.gameState} gridSize={30} />
                  </div>

                  {/* Time playing */}
                  <div className="text-center text-xs text-muted-foreground mt-2">
                    Playing for {Math.floor((Date.now() - new Date(game.startedAt).getTime()) / 60000)}m
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>
        )}

        {!isLoading && liveGames.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12"
          >
            <p className="text-muted-foreground mb-4">No live games at the moment</p>
            <Button onClick={() => navigate('/game?mode=walls')} className="neon-glow">
              Start Playing
            </Button>
          </motion.div>
        )}
      </div>
    </div>
  );
}
