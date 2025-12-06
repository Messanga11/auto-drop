'use client';

/**
 * Authentication context for admin users.
 */

import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { AdminUser, LoginRequest } from '@/types/admin';
import * as adminApi from './api';
import { setupSessionChecker } from './auth';

interface AuthContextType {
  user: AdminUser | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AdminUser | null>(null);
  const [loading, setLoading] = useState(true);

  // Check if user is authenticated on mount
  useEffect(() => {
    const checkAuth = async () => {
      const token = typeof window !== 'undefined' ? localStorage.getItem('admin_token') : null;
      if (!token) {
        setUser(null);
        setLoading(false);
        return;
      }

      try {
        const currentUser = await adminApi.getCurrentUser();
        setUser(currentUser);
      } catch (error: any) {
        // Only clear user if it's an auth error
        if (error?.status === 401 || error?.status === 403) {
          setUser(null);
          if (typeof window !== 'undefined' && !window.location.pathname.includes('/admin/login')) {
            // Don't redirect if already on login page
            window.location.href = '/admin/login';
          }
        } else {
          // For other errors, keep current user state
          console.error('Auth check error:', error);
        }
      } finally {
        // Always set loading to false, even if there's an error
        setLoading(false);
      }
    };

    // Check if we're on the login page
    const isLoginPage = typeof window !== 'undefined' && window.location.pathname === '/admin/login';
    
    if (isLoginPage) {
      // On login page, don't check auth and set loading to false immediately
      setLoading(false);
      return;
    }

    // On other pages, check authentication
    checkAuth();
    
    // Setup session expiration checker - check every 5 minutes instead of 1 minute
    const cleanup = setupSessionChecker(300000); // Check every 5 minutes
    return cleanup;
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const response = await adminApi.login(email, password);
    setUser(response.admin);
  }, []);

  const logout = useCallback(async () => {
    try {
      await adminApi.logout();
    } catch (error) {
      // Continue even if logout fails
      console.error('Logout error:', error);
    } finally {
      setUser(null);
      // Redirect to login
      if (typeof window !== 'undefined') {
        window.location.href = '/admin/login';
      }
    }
  }, []);

  const value: AuthContextType = {
    user,
    loading,
    login,
    logout,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

