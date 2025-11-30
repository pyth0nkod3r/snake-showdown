import { motion } from 'framer-motion';
import { GameMode } from '@/types/game';
import { Info } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';

interface GameInstructionsProps {
  mode: GameMode;
}

export const GameInstructions = ({ mode }: GameInstructionsProps) => {
  const instructions = {
    walls: {
      title: 'Walls Mode',
      description: 'Classic snake with boundaries',
      rules: [
        'Hitting the walls ends the game',
        'Avoid running into yourself',
        'Collect food to grow and score',
        'Speed increases every 50 points',
      ],
    },
    passthrough: {
      title: 'Pass-Through Mode',
      description: 'Snake wraps around the screen',
      rules: [
        'Pass through edges to appear on the opposite side',
        'Only avoid running into yourself',
        'Collect food to grow and score',
        'Speed increases every 50 points',
      ],
    },
  };

  const currentMode = instructions[mode];

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.3 }}
    >
      <Card className="neon-border">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <Info className="w-5 h-5 text-primary" />
            {currentMode.title}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-sm text-muted-foreground">{currentMode.description}</p>
          
          <div className="space-y-2">
            <h4 className="text-sm font-semibold text-foreground">Rules:</h4>
            <ul className="space-y-1.5">
              {currentMode.rules.map((rule, index) => (
                <li key={index} className="text-sm text-muted-foreground flex items-start gap-2">
                  <span className="text-primary mt-1">•</span>
                  <span>{rule}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="pt-2 border-t border-border">
            <h4 className="text-sm font-semibold text-foreground mb-2">Controls:</h4>
            <div className="space-y-1 text-sm text-muted-foreground">
              <p>Arrow Keys or WASD - Move</p>
              <p>Space - Pause/Resume</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
};
