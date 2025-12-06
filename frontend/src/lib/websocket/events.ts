/**
 * WebSocket event types for admin real-time updates.
 * 
 * All events follow the pattern: {type: string, data: object, timestamp: string}
 */

export type EventType =
  // Dashboard events
  | 'dashboard_stats_updated'
  // Product events
  | 'product_scraped'
  | 'score_calculated'
  // Campaign events
  | 'campaign_status_changed'
  | 'campaign_activated'
  | 'campaign_deactivated'
  // Creative events
  | 'creative_generated'
  | 'creative_status_changed'
  // Order events
  | 'order_created'
  | 'order_status_changed'
  // Action events
  | 'scraping_progress'
  | 'scraping_completed'
  | 'scraping_failed'
  | 'scoring_progress'
  | 'scoring_completed'
  | 'scoring_failed'
  | 'creative_progress'
  | 'creative_completed'
  | 'creative_failed'
  // Connection events
  | 'connection_established'
  | 'connection_closed'
  | 'reconnect_requested';

export interface WebSocketEvent<T = unknown> {
  type: EventType;
  data: T;
  timestamp: string;
}

// Event payload types
export interface DashboardStatsUpdated {
  total_products: number;
  scored_products: number;
  top_5_products: unknown[];
  active_campaigns: number;
  pending_orders: number;
}

export interface ProductScraped {
  product_id: number;
  platform: string;
  ad_id: string;
}

export interface ScoreCalculated {
  product_id: number;
  score: number;
}

export interface CampaignStatusChanged {
  campaign_id: number;
  old_status: string;
  new_status: string;
}

export interface OrderCreated {
  order_id: number;
  product_id: number;
  status: string;
}

export interface OrderStatusChanged {
  order_id: number;
  old_status: string;
  new_status: string;
}

export interface ScrapingProgress {
  progress: number; // 0-100
  ads_scraped: number;
  status: string;
}

export interface ScoringProgress {
  progress: number; // 0-100
  products_scored: number;
  status: string;
}

export interface CreativeProgress {
  product_id: number;
  progress: number; // 0-100
  status: string;
}

