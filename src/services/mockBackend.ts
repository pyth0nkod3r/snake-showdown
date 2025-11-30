import { Player, LeaderboardEntry, LiveGame, AuthUser, GameState, GameMode } from '@/types/game';

// Mock data storage
let currentUser: AuthUser | null = null;

const mockPlayers: Player[] = [
  { id: '1', username: 'SnakeMaster', score: 0, highScore: 450, gamesPlayed: 89 },
  { id: '2', username: 'NeonViper', score: 0, highScore: 380, gamesPlayed: 67 },
  { id: '3', username: 'GridRunner', score: 0, highScore: 320, gamesPlayed: 54 },
  { id: '4', username: 'ArcadeKing', score: 0, highScore: 290, gamesPlayed: 45 },
  { id: '5', username: 'PixelHunter', score: 0, highScore: 250, gamesPlayed: 38 },
];

// Centralized API service
export const mockApi = {
  // Auth endpoints
  async login(email: string, password: string): Promise<AuthUser> {
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const username = email.split('@')[0];
    currentUser = {
      id: Math.random().toString(36).substr(2, 9),
      username: username,
      email,
    };
    
    localStorage.setItem('mockUser', JSON.stringify(currentUser));
    return currentUser;
  },

  async signup(email: string, password: string, username: string): Promise<AuthUser> {
    await new Promise(resolve => setTimeout(resolve, 500));
    
    currentUser = {
      id: Math.random().toString(36).substr(2, 9),
      username,
      email,
    };
    
    localStorage.setItem('mockUser', JSON.stringify(currentUser));
    return currentUser;
  },

  async logout(): Promise<void> {
    await new Promise(resolve => setTimeout(resolve, 300));
    currentUser = null;
    localStorage.removeItem('mockUser');
  },

  async getCurrentUser(): Promise<AuthUser | null> {
    await new Promise(resolve => setTimeout(resolve, 100));
    
    if (currentUser) return currentUser;
    
    const stored = localStorage.getItem('mockUser');
    if (stored) {
      currentUser = JSON.parse(stored);
      return currentUser;
    }
    
    return null;
  },

  // Game endpoints
  async submitScore(score: number, mode: GameMode): Promise<void> {
    await new Promise(resolve => setTimeout(resolve, 300));
    console.log(`Score ${score} submitted for mode ${mode}`);
  },

  async getLeaderboard(mode: GameMode = 'walls'): Promise<LeaderboardEntry[]> {
    await new Promise(resolve => setTimeout(resolve, 400));
    
    return mockPlayers
      .sort((a, b) => b.highScore - a.highScore)
      .map((player, index) => ({
        rank: index + 1,
        username: player.username,
        score: player.highScore,
        date: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString(),
      }));
  },

  async getLiveGames(): Promise<LiveGame[]> {
    await new Promise(resolve => setTimeout(resolve, 300));
    
    // Return 3 random mock live games
    const liveGames = mockPlayers.slice(0, 3).map(player => ({
      id: Math.random().toString(36).substr(2, 9),
      player,
      gameState: this.generateMockGameState(),
      startedAt: new Date(Date.now() - Math.random() * 10 * 60 * 1000).toISOString(),
    }));
    
    return liveGames;
  },

  // Helper to generate mock game state
  generateMockGameState(): GameState {
    const score = Math.floor(Math.random() * 200);
    const snakeLength = Math.max(3, Math.floor(score / 10) + 3);
    
    const body = Array.from({ length: snakeLength }, (_, i) => ({
      x: 15 - i,
      y: 15,
    }));

    return {
      snake: {
        body,
        direction: ['UP', 'DOWN', 'LEFT', 'RIGHT'][Math.floor(Math.random() * 4)] as any,
      },
      food: {
        x: Math.floor(Math.random() * 30),
        y: Math.floor(Math.random() * 30),
      },
      score,
      isGameOver: false,
      isPaused: false,
      mode: Math.random() > 0.5 ? 'walls' : 'passthrough',
    };
  },

  // Player profile
  async getPlayerProfile(): Promise<Player | null> {
    await new Promise(resolve => setTimeout(resolve, 200));
    
    if (!currentUser) return null;
    
    return {
      id: currentUser.id,
      username: currentUser.username,
      score: 0,
      highScore: Math.floor(Math.random() * 300),
      gamesPlayed: Math.floor(Math.random() * 50),
    };
  },
};
