/**
 * API types and interfaces
 */

export interface ApiError {
  detail: string | { message: string; code?: string };
}

export interface ApiResponse<T> {
  data: T;
  error?: ApiError;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

