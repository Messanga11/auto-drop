/**
 * ApiClient - Centralized API client for all backend communications
 */

import { ApiError, PaginatedResponse } from './types';
import { handleApiError, isAuthError, ApiException } from './errorHandler';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export class ApiClient {
  private baseUrl: string;
  private getToken: () => string | null;
  private removeToken: () => void;

  constructor(
    baseUrl: string = API_BASE_URL,
    getToken: () => string | null = () => {
      if (typeof window === 'undefined') return null;
      return localStorage.getItem('admin_token');
    },
    removeToken: () => void = () => {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('admin_token');
      }
    }
  ) {
    this.baseUrl = baseUrl;
    this.getToken = getToken;
    this.removeToken = removeToken;
  }

  /**
   * Make a generic API request
   */
  async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = this.getToken();
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (token) {
      (headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers,
      });

      if (!response.ok) {
        if (response.status === 401) {
          // Unauthorized - remove token and redirect to login
          this.removeToken();
          if (typeof window !== 'undefined') {
            window.location.href = '/admin/login';
          }
          throw new ApiException('Unauthorized', 401);
        }

        let errorData: ApiError;
        try {
          errorData = await response.json();
        } catch {
          errorData = { detail: response.statusText };
        }

        throw new ApiException(
          typeof errorData.detail === 'string'
            ? errorData.detail
            : errorData.detail.message || 'API request failed',
          response.status
        );
      }

      return response.json();
    } catch (error) {
      if (error instanceof ApiException) {
        throw error;
      }
      throw handleApiError(error);
    }
  }

  /**
   * GET request
   */
  async get<T>(endpoint: string, params?: Record<string, any>): Promise<T> {
    const url = new URL(endpoint, this.baseUrl);
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          url.searchParams.append(key, String(value));
        }
      });
    }

    return this.request<T>(url.pathname + url.search, {
      method: 'GET',
    });
  }

  /**
   * POST request
   */
  async post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  /**
   * PATCH request
   */
  async patch<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  /**
   * DELETE request
   */
  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'DELETE',
    });
  }

  /**
   * Handle error (for backward compatibility)
   */
  handleError(error: unknown): Error {
    return handleApiError(error);
  }
}

// Default instance
export const apiClient = new ApiClient();

