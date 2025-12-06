/**
 * Admin authentication utilities.
 */

import { getCurrentUser } from './api';

/**
 * Get authentication token from localStorage.
 */
function getToken(): string | null {
  if (typeof window === 'undefined') {
    return null;
  }
  return localStorage.getItem('admin_token');
}

/**
 * Remove authentication token from localStorage.
 */
function removeToken(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('admin_token');
  }
}

/**
 * Check if user is authenticated.
 */
export function isAuthenticated(): boolean {
  return getToken() !== null;
}

/**
 * Get authentication token.
 */
export function getAuthToken(): string | null {
  return getToken();
}

/**
 * Clear authentication (logout).
 */
export function clearAuth(): void {
  removeToken();
}

/**
 * Check if session is expired and handle it.
 */
export async function checkSessionExpiration(): Promise<boolean> {
  const token = getToken();
  if (!token) {
    return false;
  }

  try {
    // Try to decode token to check expiration
    const payload = JSON.parse(atob(token.split('.')[1]));
    const exp = payload.exp * 1000; // Convert to milliseconds
    const now = Date.now();

    if (now >= exp) {
      // Token expired
      clearAuth();
      if (typeof window !== 'undefined') {
        window.location.href = '/admin/login';
      }
      return false;
    }

    // Verify token is still valid by calling /auth/me
    await getCurrentUser();
    return true;
  } catch (error) {
    // Token invalid or expired
    clearAuth();
    if (typeof window !== 'undefined') {
      window.location.href = '/admin/login';
    }
    return false;
  }
}

/**
 * Setup session expiration checker.
 */
export function setupSessionChecker(intervalMs: number = 60000): () => void {
  let intervalId: NodeJS.Timeout | null = null;

  if (typeof window !== 'undefined') {
    intervalId = setInterval(() => {
      checkSessionExpiration().catch(console.error);
    }, intervalMs);

    // Also check on visibility change
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        checkSessionExpiration().catch(console.error);
      }
    };
    document.addEventListener('visibilitychange', handleVisibilityChange);

    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }

  return () => {};
}

