/**
 * TypeScript types for Admin Dashboard Application
 */

export interface AdminUser {
  id: number;
  email: string;
  is_active: boolean;
  created_at: string;
  last_login_at: string | null;
}

export interface AdminSession {
  token: string;
  expires_at: string;
  admin: AdminUser;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  expires_at: string;
  admin: AdminUser;
}

export interface DashboardStats {
  total_products: number;
  scored_products: number;
  top_5_products: Array<{
    id: number;
    product_id: number;
    total_score: number;
    engagement_rate: number;
    calculated_at: string | null;
  }>;
  active_campaigns: number;
  pending_orders: number;
  total_campaigns: number;
  total_orders: number;
  total_creatives: number;
}

export interface Product {
  id: number;
  platform: string;
  ad_id: string | null;
  page_name: string | null;
  advertiser_name: string | null;
  caption: string | null;
  likes: number;
  comments: number;
  shares: number;
  views: number;
  scraped_at: string;
  scored: boolean;
  selected_for_campaign: boolean;
  score: number | null;
  engagement_rate: number | null;
}

export interface Campaign {
  id: number;
  product_id: number;
  platform: 'meta' | 'tiktok';
  campaign_name: string;
  status: 'paused' | 'active' | 'completed';
  daily_budget: number;
  created_at: string;
  activated_at: string | null;
}

export interface Creative {
  id: number;
  product_id: number;
  video_type: 'ugc' | 'problem_solution' | 'short_hook' | 'carousel';
  status: 'queued' | 'processing' | 'completed' | 'failed';
  created_at: string;
  completed_at: string | null;
}

export interface Order {
  id: number;
  product_id: number;
  product_name: string;
  full_name: string;
  phone: string;
  quantity: number;
  status: 'pending' | 'confirmed' | 'shipped' | 'delivered';
  created_at: string;
  updated_at: string;
}

export interface ActionStatus {
  status: 'idle' | 'running' | 'completed' | 'failed';
  progress: number;
  ads_scraped?: number;
}

export interface AdminAction {
  id: number;
  admin_id: number;
  action_type: string;
  resource_type: string | null;
  resource_id: number | null;
  result: 'success' | 'failure' | 'partial';
  details: Record<string, unknown> | null;
  created_at: string;
}

