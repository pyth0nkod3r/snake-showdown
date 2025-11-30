import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mockApi } from './mockBackend';

describe('Mock Backend API', () => {
  beforeEach(() => {
    localStorage.clear();
    vi.clearAllMocks();
  });

  describe('Authentication', () => {
    it('should login user successfully', async () => {
      const user = await mockApi.login('test@example.com', 'password123');
      
      expect(user).toBeDefined();
      expect(user.email).toBe('test@example.com');
      expect(user.username).toBe('test');
    });

    it('should signup user successfully', async () => {
      const user = await mockApi.signup('new@example.com', 'password123', 'NewUser');
      
      expect(user).toBeDefined();
      expect(user.email).toBe('new@example.com');
      expect(user.username).toBe('NewUser');
    });

    it('should logout user', async () => {
      await mockApi.login('test@example.com', 'password123');
      await mockApi.logout();
      
      const currentUser = await mockApi.getCurrentUser();
      expect(currentUser).toBeNull();
    });

    it('should get current user from localStorage', async () => {
      await mockApi.login('test@example.com', 'password123');
      const user = await mockApi.getCurrentUser();
      
      expect(user).toBeDefined();
      expect(user?.email).toBe('test@example.com');
    });
  });

  describe('Game Data', () => {
    it('should submit score successfully', async () => {
      await expect(mockApi.submitScore(150, 'walls')).resolves.not.toThrow();
    });

    it('should return leaderboard entries', async () => {
      const leaderboard = await mockApi.getLeaderboard('walls');
      
      expect(leaderboard).toBeInstanceOf(Array);
      expect(leaderboard.length).toBeGreaterThan(0);
      expect(leaderboard[0]).toHaveProperty('rank');
      expect(leaderboard[0]).toHaveProperty('username');
      expect(leaderboard[0]).toHaveProperty('score');
    });

    it('should return live games', async () => {
      const liveGames = await mockApi.getLiveGames();
      
      expect(liveGames).toBeInstanceOf(Array);
      expect(liveGames.length).toBe(3);
      expect(liveGames[0]).toHaveProperty('player');
      expect(liveGames[0]).toHaveProperty('gameState');
    });

    it('should get player profile', async () => {
      await mockApi.login('test@example.com', 'password123');
      const profile = await mockApi.getPlayerProfile();
      
      expect(profile).toBeDefined();
      expect(profile?.username).toBe('test');
      expect(profile?.highScore).toBeGreaterThanOrEqual(0);
    });
  });

  describe('Mock Game State Generation', () => {
    it('should generate valid game state', () => {
      const gameState = mockApi.generateMockGameState();
      
      expect(gameState).toHaveProperty('snake');
      expect(gameState).toHaveProperty('food');
      expect(gameState).toHaveProperty('score');
      expect(gameState.snake.body.length).toBeGreaterThan(0);
      expect(gameState.food.x).toBeGreaterThanOrEqual(0);
      expect(gameState.food.y).toBeGreaterThanOrEqual(0);
    });
  });
});
