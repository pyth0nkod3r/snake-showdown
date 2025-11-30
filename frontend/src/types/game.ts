export type GameMode = 'passthrough' | 'walls';

export type Direction = 'UP' | 'DOWN' | 'LEFT' | 'RIGHT';

export interface Position {
  x: number;
  y: number;
}

export interface Snake {
  body: Position[];
  direction: Direction;
}

export interface GameState {
  snake: Snake;
  food: Position;
  score: number;
  isGameOver: boolean;
  isPaused: boolean;
  mode: GameMode;
}

export interface Player {
  id: string;
  username: string;
  score: number;
  highScore: number;
  gamesPlayed: number;
}

export interface LeaderboardEntry {
  rank: number;
  username: string;
  score: number;
  date: string;
}

export interface LiveGame {
  id: string;
  player: Player;
  gameState: GameState;
  startedAt: string;
}

export interface AuthUser {
  id: string;
  username: string;
  email: string;
}

export interface AuthResponse {
  user: AuthUser;
  token: string;
}

export interface ScoreResponse {
  message: string;
  isNewHighScore: boolean;
  rank: number;
}

export interface LeaderboardResponse {
  entries: LeaderboardEntry[];
  total: number;
}

