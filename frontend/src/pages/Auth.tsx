import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card } from '@/components/ui/card';
import { mockApi } from '@/services/mockBackend';
import { ApiError } from '@/services/api';
import { useToast } from '@/hooks/use-toast';
import { Zap } from 'lucide-react';

export default function Auth() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      if (isLogin) {
        await mockApi.login(email, password);
        toast({
          title: 'Welcome back!',
          description: 'Successfully logged in.',
        });
      } else {
        await mockApi.signup(email, password, username);
        toast({
          title: 'Account created!',
          description: 'Welcome to Neon Snake.',
        });
      }
      navigate('/');
    } catch (error) {
      // Get specific error message from API
      let errorMessage = 'Something went wrong. Please try again.';

      if (error instanceof ApiError) {
        errorMessage = error.message;
      } else if (error instanceof Error) {
        errorMessage = error.message;
      }

      toast({
        title: 'Error',
        description: errorMessage,
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 grid-pattern">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md"
      >
        <div className="text-center mb-8">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', bounce: 0.5 }}
            className="inline-block mb-4"
          >
            <Zap className="w-16 h-16 text-primary neon-glow" />
          </motion.div>
          <h1 className="text-5xl font-bold text-primary neon-text mb-2">NEON SNAKE</h1>
          <p className="text-muted-foreground">Enter the grid</p>
        </div>

        <Card className="p-6 border-primary/20 neon-glow bg-card/50 backdrop-blur">
          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLogin && (
              <div className="space-y-2">
                <Label htmlFor="username">Username</Label>
                <Input
                  id="username"
                  type="text"
                  placeholder="SnakeMaster"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                  className="bg-input border-border"
                />
              </div>
            )}

            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="player@neon.game"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="bg-input border-border"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="bg-input border-border"
              />
            </div>

            <Button
              type="submit"
              className="w-full neon-glow"
              disabled={isLoading}
            >
              {isLoading ? 'Loading...' : isLogin ? 'Login' : 'Sign Up'}
            </Button>
          </form>

          <div className="mt-6 text-center space-y-3">
            <button
              type="button"
              onClick={() => setIsLogin(!isLogin)}
              className="text-sm text-primary hover:underline"
            >
              {isLogin ? "Don't have an account? Sign up" : 'Already have an account? Login'}
            </button>
            
            {isLogin && (
              <p className="text-xs text-muted-foreground">
                Demo: Try <span className="text-primary">snake@example.com</span> / <span className="text-primary">demo123</span>
              </p>
            )}
          </div>
        </Card>
      </motion.div>
    </div>
  );
}
