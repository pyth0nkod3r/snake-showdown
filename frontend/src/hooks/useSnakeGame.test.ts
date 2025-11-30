import { describe, it, expect } from 'vitest';
import { gameUtils } from './useSnakeGame';

const { getNextHead, checkCollision, generateFood, GRID_SIZE } = gameUtils;

describe('Snake Game Logic', () => {
  describe('getNextHead', () => {
    it('should move head up correctly', () => {
      const head = { x: 5, y: 5 };
      const newHead = getNextHead(head, 'UP');
      expect(newHead).toEqual({ x: 5, y: 4 });
    });

    it('should move head down correctly', () => {
      const head = { x: 5, y: 5 };
      const newHead = getNextHead(head, 'DOWN');
      expect(newHead).toEqual({ x: 5, y: 6 });
    });

    it('should move head left correctly', () => {
      const head = { x: 5, y: 5 };
      const newHead = getNextHead(head, 'LEFT');
      expect(newHead).toEqual({ x: 4, y: 5 });
    });

    it('should move head right correctly', () => {
      const head = { x: 5, y: 5 };
      const newHead = getNextHead(head, 'RIGHT');
      expect(newHead).toEqual({ x: 6, y: 5 });
    });
  });

  describe('checkCollision', () => {
    it('should detect collision with snake body', () => {
      const head = { x: 5, y: 5 };
      const body = [
        { x: 5, y: 5 },
        { x: 4, y: 5 },
        { x: 3, y: 5 },
      ];
      expect(checkCollision(head, body)).toBe(true);
    });

    it('should not detect collision when head is clear', () => {
      const head = { x: 5, y: 5 };
      const body = [
        { x: 4, y: 5 },
        { x: 3, y: 5 },
        { x: 2, y: 5 },
      ];
      expect(checkCollision(head, body)).toBe(false);
    });

    it('should handle empty body', () => {
      const head = { x: 5, y: 5 };
      const body: any[] = [];
      expect(checkCollision(head, body)).toBe(false);
    });
  });

  describe('generateFood', () => {
    it('should generate food within grid boundaries', () => {
      const body = [{ x: 5, y: 5 }];
      const food = generateFood(body);
      
      expect(food.x).toBeGreaterThanOrEqual(0);
      expect(food.x).toBeLessThan(GRID_SIZE);
      expect(food.y).toBeGreaterThanOrEqual(0);
      expect(food.y).toBeLessThan(GRID_SIZE);
    });

    it('should not generate food on snake body', () => {
      const body = [{ x: 5, y: 5 }];
      const food = generateFood(body);
      
      expect(food.x === 5 && food.y === 5).toBe(false);
    });

    it('should generate valid food for large snake', () => {
      const body = Array.from({ length: 20 }, (_, i) => ({ x: i, y: 0 }));
      const food = generateFood(body);
      
      const isOnSnake = body.some(segment => 
        segment.x === food.x && segment.y === food.y
      );
      expect(isOnSnake).toBe(false);
    });
  });
});
