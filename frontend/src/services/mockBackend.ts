import {
  Player,
  LeaderboardEntry,
  LiveGame,
  AuthUser,
  GameMode,
  AuthResponse,
  ScoreResponse,
  LeaderboardResponse,
} from '@/types/game';
import * as api from './api';

// Centralized API service
export const mockApi = {
  // Auth endpoints
  async login(email: string, password: string): Promise<AuthUser> {
    const response = await api.post<AuthResponse>('/auth/login', {
      email,
      password,
    });

    // Store token
    api.setAuthToken(response.token);

    return response.user;
  },

  async signup(email: string, password: string, username: string): Promise<AuthUser> {
    const response = await api.post<AuthResponse>('/auth/signup', {
      email,
      password,
      username,
    });

    // Store token
    api.setAuthToken(response.token);

    return response.user;
  },

  async logout(): Promise<void> {
    try {
      await api.post<void>('/auth/logout');
    } finally {
      // Always clear token even if request fails
      api.clearAuthToken();
    }
  },

  async getCurrentUser(): Promise<AuthUser | null> {
    try {
      const user = await api.get<AuthUser>('/auth/me');
      return user;
    } catch (error) {
      // If unauthorized or any error, return null
      if (error instanceof api.ApiError && error.status === 401) {
        api.clearAuthToken();
      }
      return null;
    }
  },

  // Game endpoints
  async submitScore(score: number, mode: GameMode): Promise<void> {
    await api.post<ScoreResponse>('/game/score', {
      score,
      mode,
    });
  },

  async getLeaderboard(mode: GameMode = 'walls'): Promise<LeaderboardEntry[]> {
    const response = await api.get<LeaderboardResponse>(
      `/game/leaderboard?mode=${mode}&limit=10&offset=0`
    );
    return response.entries;
  },

  async getLiveGames(): Promise<LiveGame[]> {
    const games = await api.get<LiveGame[]>('/game/live?limit=10');
    return games;
  },

  // Player profile
  async getPlayerProfile(): Promise<Player | null> {
    try {
      const player = await api.get<Player>('/player/profile');
      return player;
    } catch (error) {
      if (error instanceof api.ApiError && error.status === 404) {
        return null;
      }
      throw error;
    }
  },
};
