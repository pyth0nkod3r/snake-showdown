import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { mockApi } from '@/services/mockBackend';
import { AuthUser } from '@/types/game';
import { Zap, Trophy, Eye, Play, LogOut, LogIn } from 'lucide-react';

const Index = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      const currentUser = await mockApi.getCurrentUser();
      setUser(currentUser);
      setIsLoading(false);
    };

    loadUser();
  }, []);

  const handleLogout = async () => {
    await mockApi.logout();
    setUser(null);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center grid-pattern">
        <div className="text-muted-foreground">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 grid-pattern">
      {/* Header with user info */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="absolute top-8 right-8"
      >
        {user ? (
          <div className="flex items-center gap-4">
            <div className="text-right">
              <div className="text-sm text-muted-foreground">Logged in as</div>
              <div className="font-bold text-primary">{user.username}</div>
            </div>
            <Button variant="outline" size="sm" onClick={handleLogout} className="neon-glow">
              <LogOut className="w-4 h-4" />
            </Button>
          </div>
        ) : (
          <Button variant="outline" onClick={() => navigate('/auth')} className="neon-glow">
            <LogIn className="w-4 h-4 mr-2" />
            Login
          </Button>
        )}
      </motion.div>

      <div className="max-w-4xl w-full">
        {/* Logo and title */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', bounce: 0.5 }}
          className="text-center mb-12"
        >
          <Zap className="w-24 h-24 text-primary neon-glow mx-auto mb-6" />
          <h1 className="text-7xl font-bold text-primary neon-text mb-4">NEON SNAKE</h1>
          <p className="text-xl text-muted-foreground">Classic arcade. Modern twist.</p>
        </motion.div>

        {/* Game mode selection */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Card className="p-8 border-primary/20 neon-glow bg-card/50 backdrop-blur hover:bg-card/70 transition-colors cursor-pointer group"
                  onClick={() => navigate('/game?mode=walls')}>
              <div className="text-center space-y-4">
                <div className="text-4xl font-bold text-primary group-hover:neon-text transition-all">
                  WALLS MODE
                </div>
                <p className="text-muted-foreground">
                  Classic gameplay. Hit the wall, game over.
                </p>
                <Button className="w-full neon-glow" size="lg">
                  <Play className="w-5 h-5 mr-2" />
                  Play Walls
                </Button>
              </div>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
          >
            <Card className="p-8 border-secondary/20 neon-glow-secondary bg-card/50 backdrop-blur hover:bg-card/70 transition-colors cursor-pointer group"
                  onClick={() => navigate('/game?mode=passthrough')}>
              <div className="text-center space-y-4">
                <div className="text-4xl font-bold text-secondary group-hover:neon-text transition-all">
                  PASS-THROUGH
                </div>
                <p className="text-muted-foreground">
                  No walls. Snake wraps around the edges.
                </p>
                <Button className="w-full neon-glow-secondary bg-secondary text-secondary-foreground hover:bg-secondary/90" size="lg">
                  <Play className="w-5 h-5 mr-2" />
                  Play Pass-Through
                </Button>
              </div>
            </Card>
          </motion.div>
        </div>

        {/* Action buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="grid md:grid-cols-2 gap-4"
        >
          <Button
            variant="outline"
            size="lg"
            onClick={() => navigate('/leaderboard')}
            className="neon-glow"
          >
            <Trophy className="w-5 h-5 mr-2" />
            Leaderboard
          </Button>

          <Button
            variant="outline"
            size="lg"
            onClick={() => navigate('/spectate')}
            className="neon-glow-accent"
          >
            <Eye className="w-5 h-5 mr-2" />
            Watch Live Games
          </Button>
        </motion.div>

        {/* Auth prompt for guests */}
        {!user && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 }}
            className="text-center mt-8"
          >
            <p className="text-muted-foreground mb-2">
              Want to save your high scores?
            </p>
            <Button variant="link" onClick={() => navigate('/auth')} className="text-primary">
              Create an account →
            </Button>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default Index;
