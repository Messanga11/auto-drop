/**
 * Admin API client - Refactored to use centralized ApiClient
 */

import { LoginRequest, LoginResponse, AdminUser, DashboardStats, Product, Campaign, Creative, Order } from '@/types/admin';
import { apiClient } from '@/lib/api/client';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

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
 * Set authentication token in localStorage.
 */
function setToken(token: string): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem('admin_token', token);
  }
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
 * Login admin user.
 */
export async function login(email: string, password: string): Promise<LoginResponse> {
  const response = await fetch(`${API_BASE_URL}/admin/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password } as LoginRequest),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || `Login failed: ${response.statusText}`);
  }

  const data: LoginResponse = await response.json();
  setToken(data.token);
  return data;
}

/**
 * Logout admin user.
 */
export async function logout(): Promise<void> {
  await apiClient.post('/admin/auth/logout');
  removeToken();
}

/**
 * Get current admin user.
 */
export async function getCurrentUser(): Promise<AdminUser> {
  try {
    return await apiClient.get<AdminUser>('/admin/auth/me');
  } catch (error) {
    // If unauthorized, remove token
    removeToken();
    throw error;
  }
}

/**
 * Get dashboard statistics.
 */
export async function getDashboardStats(): Promise<DashboardStats> {
  return apiClient.get<DashboardStats>('/admin/dashboard/stats');
}

/**
 * Get products list.
 */
export async function getProducts(params?: {
  platform?: string;
  scored?: boolean;
  min_score?: number;
  page?: number;
  page_size?: number;
}): Promise<{ products: Product[]; total: number; page: number; page_size: number }> {
  return apiClient.get<{ products: Product[]; total: number; page: number; page_size: number }>(
    '/admin/products',
    params
  );
}

/**
 * Get campaigns list.
 */
export async function getCampaigns(params?: {
  status?: string;
  platform?: string;
  page?: number;
  page_size?: number;
}): Promise<{ campaigns: Campaign[]; total: number }> {
  return apiClient.get<{ campaigns: Campaign[]; total: number }>('/admin/campaigns', params);
}

/**
 * Activate campaign.
 */
export async function activateCampaign(campaignId: number): Promise<Campaign> {
  return apiClient.post<Campaign>(`/admin/campaigns/${campaignId}/activate`);
}

/**
 * Deactivate campaign.
 */
export async function deactivateCampaign(campaignId: number): Promise<Campaign> {
  return apiClient.post<Campaign>(`/admin/campaigns/${campaignId}/deactivate`);
}

/**
 * Get creatives list.
 */
export async function getCreatives(params?: {
  product_id?: number;
  status?: string;
  page?: number;
  page_size?: number;
}): Promise<{ creatives: Creative[]; total: number }> {
  return apiClient.get<{ creatives: Creative[]; total: number }>('/admin/creatives', params);
}

/**
 * Get orders list.
 */
export async function getOrders(params?: {
  status?: string;
  date_from?: string;
  date_to?: string;
  page?: number;
  page_size?: number;
}): Promise<{ orders: Order[]; total: number }> {
  return apiClient.get<{ orders: Order[]; total: number }>('/admin/orders', params);
}

/**
 * Update order status.
 */
export async function updateOrderStatus(orderId: number, status: 'pending' | 'confirmed' | 'shipped' | 'delivered'): Promise<Order> {
  return apiClient.patch<Order>(`/admin/orders/${orderId}/status`, { status });
}

/**
 * Start scraping action.
 */
export async function startScraping(platform: 'facebook' | 'tiktok'): Promise<{ message: string }> {
  return apiClient.post<{ message: string }>(`/admin/actions/scraping/start?platform=${platform}`);
}

/**
 * Get scraping status.
 */
export async function getScrapingStatus(): Promise<{ status: string; progress: number; ads_scraped: number }> {
  return apiClient.get<{ status: string; progress: number; ads_scraped: number }>('/admin/actions/scraping/status');
}

/**
 * Calculate scoring.
 */
export async function calculateScoring(): Promise<{ message: string }> {
  return apiClient.post<{ message: string }>('/admin/actions/scoring/calculate');
}

/**
 * Generate creatives for a product.
 */
export async function generateCreatives(productId: number): Promise<{ message: string }> {
  return apiClient.post<{ message: string }>(`/admin/actions/creatives/generate/${productId}`);
}
