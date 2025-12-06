/**
 * Error handler utility for API errors
 */

import { ApiError } from './types';

export class ApiException extends Error {
  constructor(
    message: string,
    public status?: number,
    public code?: string
  ) {
    super(message);
    this.name = 'ApiException';
  }
}

/**
 * Handle API error response
 */
export function handleApiError(error: unknown): Error {
  if (error instanceof ApiException) {
    return error;
  }

  if (error instanceof Error) {
    return error;
  }

  if (typeof error === 'object' && error !== null) {
    const apiError = error as ApiError;
    if (apiError.detail) {
      const message =
        typeof apiError.detail === 'string'
          ? apiError.detail
          : apiError.detail.message || 'Unknown error';
      return new ApiException(message, undefined, (apiError.detail as any)?.code);
    }
  }

  return new Error('Unknown error occurred');
}

/**
 * Check if error is an authentication error (401)
 */
export function isAuthError(error: unknown): boolean {
  if (error instanceof ApiException) {
    return error.status === 401;
  }
  return false;
}

