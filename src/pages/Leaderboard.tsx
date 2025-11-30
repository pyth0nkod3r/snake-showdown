import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { mockApi } from '@/services/mockBackend';
import { LeaderboardEntry } from '@/types/game';
import { ArrowLeft, Trophy, Medal, Award } from 'lucide-react';

export default function Leaderboard() {
  const navigate = useNavigate();
  const [entries, setEntries] = useState<LeaderboardEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadLeaderboard = async () => {
      const data = await mockApi.getLeaderboard();
      setEntries(data);
      setIsLoading(false);
    };

    loadLeaderboard();
  }, []);

  const getRankIcon = (rank: number) => {
    switch (rank) {
      case 1:
        return <Trophy className="w-6 h-6 text-accent" />;
      case 2:
        return <Medal className="w-6 h-6 text-primary" />;
      case 3:
        return <Award className="w-6 h-6 text-secondary" />;
      default:
        return <span className="text-muted-foreground font-bold">#{rank}</span>;
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

          <h1 className="text-4xl font-bold text-primary neon-text">LEADERBOARD</h1>
          
          <div className="w-24" /> {/* Spacer */}
        </motion.div>

        {/* Leaderboard */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <Card className="p-6 border-primary/20 neon-glow bg-card/50 backdrop-blur">
            {isLoading ? (
              <div className="text-center py-12">
                <div className="text-muted-foreground">Loading scores...</div>
              </div>
            ) : (
              <div className="space-y-3">
                {entries.map((entry, index) => (
                  <motion.div
                    key={entry.rank}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className={`flex items-center justify-between p-4 rounded border ${
                      entry.rank <= 3
                        ? 'border-primary/40 bg-primary/5'
                        : 'border-border bg-muted/20'
                    }`}
                  >
                    <div className="flex items-center gap-4 flex-1">
                      <div className="w-12 flex justify-center">
                        {getRankIcon(entry.rank)}
                      </div>
                      
                      <div className="flex-1">
                        <div className="font-semibold text-foreground">{entry.username}</div>
                        <div className="text-xs text-muted-foreground">
                          {new Date(entry.date).toLocaleDateString()}
                        </div>
                      </div>
                    </div>

                    <div className="text-2xl font-bold text-primary">
                      {entry.score}
                    </div>
                  </motion.div>
                ))}
              </div>
            )}
          </Card>
        </motion.div>
      </div>
    </div>
  );
}
