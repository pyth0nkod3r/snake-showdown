import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import { mockApi } from './mockBackend';
import * as api from './api';

// Mock fetch globally
const mockFetch = vi.fn();
global.fetch = mockFetch;

// Mock localStorage for testing
const localStorageMock = (() => {
  let store: Record<string, string> = {};
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => {
      store[key] = value;
    },
    removeItem: (key: string) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    }
  };
})();

Object.defineProperty(global, 'localStorage', {
  value: localStorageMock,
  writable: true
});

describe('Backend API Integration', () => {
  beforeEach(() => {
    localStorageMock.clear();
    vi.clearAllMocks();
    mockFetch.mockClear();
  });

  afterEach(() => {
    api.clearAuthToken();
  });

  describe('Authentication', () => {
    it('should login user successfully and store token', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({
          user: {
            id: '123',
            username: 'testuser',
            email: 'test@example.com'
          },
          token: 'test-token-123'
        })
      });

      const user = await mockApi.login('test@example.com', 'password123');

      expect(user).toBeDefined();
      expect(user.email).toBe('test@example.com');
      expect(user.username).toBe('testuser');
      expect(localStorageMock.getItem('auth_token')).toBe('test-token-123');
      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:3000/api/auth/login',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ email: 'test@example.com', password: 'password123' })
        })
      );
    });

    it('should signup user successfully and store token', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({
          user: {
            id: '456',
            username: 'NewUser',
            email: 'new@example.com'
          },
          token: 'signup-token-456'
        })
      });

      const user = await mockApi.signup('new@example.com', 'password123', 'NewUser');

      expect(user).toBeDefined();
      expect(user.email).toBe('new@example.com');
      expect(user.username).toBe('NewUser');
      expect(localStorageMock.getItem('auth_token')).toBe('signup-token-456');
    });

    it('should logout user and clear token', async () => {
      localStorageMock.setItem('auth_token', 'test-token');

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({ message: 'Logged out' })
      });

      await mockApi.logout();

      expect(localStorageMock.getItem('auth_token')).toBeNull();
      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:3000/api/auth/logout',
        expect.objectContaining({
          method: 'POST'
        })
      );
    });

    it('should get current user with valid token', async () => {
      localStorageMock.setItem('auth_token', 'valid-token');

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({
          id: '123',
          username: 'testuser',
          email: 'test@example.com'
        })
      });

      const user = await mockApi.getCurrentUser();

      expect(user).toBeDefined();
      expect(user?.email).toBe('test@example.com');

      // Check that fetch was called with correct auth header
      expect(mockFetch).toHaveBeenCalledTimes(1);
      const [url, options] = mockFetch.mock.calls[0];
      expect(url).toBe('http://localhost:3000/api/auth/me');
      expect(options.headers['Authorization']).toBe('Bearer valid-token');
    });

    it('should return null and clear token on 401', async () => {
      localStorageMock.setItem('auth_token', 'invalid-token');

      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 401,
        json: async () => ({ detail: 'Unauthorized' })
      });

      const user = await mockApi.getCurrentUser();

      expect(user).toBeNull();
      expect(localStorageMock.getItem('auth_token')).toBeNull();
    });
  });

  describe('Game Data', () => {
    it('should submit score successfully', async () => {
      localStorage.setItem('auth_token', 'valid-token');

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 201,
        json: async () => ({
          message: 'Score submitted',
          isNewHighScore: true,
          rank: 5
        })
      });

      await expect(mockApi.submitScore(150, 'walls')).resolves.not.toThrow();

      expect(mockFetch).toHaveBeenCalledWith(
        'http://localhost:3000/api/game/score',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ score: 150, mode: 'walls' })
        })
      );
    });

    it('should return leaderboard entries', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({
          entries: [
            { rank: 1, username: 'SnakeMaster', score: 450, date: '2024-01-01T00:00:00Z' },
            { rank: 2, username: 'NeonViper', score: 380, date: '2024-01-02T00:00:00Z' }
          ],
          total: 2
        })
      });

      const leaderboard = await mockApi.getLeaderboard('walls');

      expect(leaderboard).toBeInstanceOf(Array);
      expect(leaderboard.length).toBe(2);
      expect(leaderboard[0]).toHaveProperty('rank');
      expect(leaderboard[0]).toHaveProperty('username');
      expect(leaderboard[0]).toHaveProperty('score');
      expect(leaderboard[0].username).toBe('SnakeMaster');
    });

    it('should return live games', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ([
          {
            id: 'game1',
            player: { id: '1', username: 'Player1', score: 0, highScore: 100, gamesPlayed: 5 },
            gameState: {
              snake: { body: [{ x: 10, y: 10 }], direction: 'UP' },
              food: { x: 5, y: 5 },
              score: 50,
              isGameOver: false,
              isPaused: false,
              mode: 'walls'
            },
            startedAt: '2024-01-01T00:00:00Z'
          }
        ])
      });

      const liveGames = await mockApi.getLiveGames();

      expect(liveGames).toBeInstanceOf(Array);
      expect(liveGames.length).toBe(1);
      expect(liveGames[0]).toHaveProperty('player');
      expect(liveGames[0]).toHaveProperty('gameState');
    });

    it('should get player profile', async () => {
      localStorage.setItem('auth_token', 'valid-token');

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({
          id: '123',
          username: 'testuser',
          score: 0,
          highScore: 250,
          gamesPlayed: 10
        })
      });

      const profile = await mockApi.getPlayerProfile();

      expect(profile).toBeDefined();
      expect(profile?.username).toBe('testuser');
      expect(profile?.highScore).toBe(250);
    });

    it('should return null for 404 player profile', async () => {
      localStorage.setItem('auth_token', 'valid-token');

      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
        json: async () => ({ detail: 'Not found' })
      });

      const profile = await mockApi.getPlayerProfile();

      expect(profile).toBeNull();
    });
  });
});
