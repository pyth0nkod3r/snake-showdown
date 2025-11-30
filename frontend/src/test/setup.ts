import { expect, afterEach, vi, beforeAll } from 'vitest';
import { cleanup } from '@testing-library/react';
import '@testing-library/jest-dom';

// Suppress canvas-related warnings in tests
beforeAll(() => {
  const originalError = console.error;
  vi.spyOn(console, 'error').mockImplementation((...args) => {
    const errorMessage = args[0]?.toString() || '';
    // Suppress canvas warnings
    if (errorMessage.includes("Not implemented: HTMLCanvasElement's getContext()")) {
      return;
    }
    originalError(...args);
  });
});

afterEach(() => {
  cleanup();
});

// Mock localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
};

global.localStorage = localStorageMock as any;
