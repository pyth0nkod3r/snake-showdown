/**
 * Centralized API client for Snake Showdown backend.
 * Handles authentication, request/response interception, and error handling.
 */

// Use environment variable for API base URL, fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api';

/**
 * Custom error class for API errors
 */
export class ApiError extends Error {
    constructor(
        public status: number,
        message: string,
        public data?: unknown
    ) {
        super(message);
        this.name = 'ApiError';
    }
}

/**
 * Get authentication token from localStorage
 */
function getAuthToken(): string | null {
    return localStorage.getItem('auth_token');
}

/**
 * Set authentication token in localStorage
 */
export function setAuthToken(token: string): void {
    localStorage.setItem('auth_token', token);
}

/**
 * Clear authentication token from localStorage
 */
export function clearAuthToken(): void {
    localStorage.removeItem('auth_token');
}

/**
 * Make an authenticated API request
 */
async function apiRequest<T>(
    endpoint: string,
    options: RequestInit = {}
): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    const token = getAuthToken();

    // Prepare headers
    const headers: HeadersInit = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    // Add authorization header if token exists
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(url, {
            ...options,
            headers,
        });

        // Handle error responses
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));

            // Handle 401 Unauthorized - clear token and redirect to login
            if (response.status === 401) {
                clearAuthToken();
                // Let the component handle the redirect
            }

            throw new ApiError(
                response.status,
                errorData.detail || errorData.message || `HTTP ${response.status}`,
                errorData
            );
        }

        // Handle 204 No Content
        if (response.status === 204) {
            return {} as T;
        }

        // Parse JSON response
        return await response.json();
    } catch (error) {
        // Re-throw ApiError as-is
        if (error instanceof ApiError) {
            throw error;
        }

        // Handle network errors
        if (error instanceof TypeError) {
            throw new ApiError(0, 'Network error - unable to reach server');
        }

        // Handle other errors
        throw new ApiError(500, error instanceof Error ? error.message : 'Unknown error');
    }
}

/**
 * HTTP GET request
 */
export async function get<T>(endpoint: string): Promise<T> {
    return apiRequest<T>(endpoint, { method: 'GET' });
}

/**
 * HTTP POST request
 */
export async function post<T>(endpoint: string, data?: unknown): Promise<T> {
    return apiRequest<T>(endpoint, {
        method: 'POST',
        body: data ? JSON.stringify(data) : undefined,
    });
}

/**
 * HTTP PUT request
 */
export async function put<T>(endpoint: string, data?: unknown): Promise<T> {
    return apiRequest<T>(endpoint, {
        method: 'PUT',
        body: data ? JSON.stringify(data) : undefined,
    });
}

/**
 * HTTP DELETE request
 */
export async function del<T>(endpoint: string): Promise<T> {
    return apiRequest<T>(endpoint, { method: 'DELETE' });
}

/**
 * HTTP PATCH request
 */
export async function patch<T>(endpoint: string, data?: unknown): Promise<T> {
    return apiRequest<T>(endpoint, {
        method: 'PATCH',
        body: data ? JSON.stringify(data) : undefined,
    });
}
