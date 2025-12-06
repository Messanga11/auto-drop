/**
 * React hooks for WebSocket client.
 */

import { useEffect, useRef, useState, useCallback } from 'react';
import { WebSocketClient, ConnectionStatus, MessageHandler } from './client';
import { WebSocketEvent, EventType } from './events';
import { DashboardStats, Product, Campaign, Order } from '@/types/admin';

/**
 * Hook to manage WebSocket connection.
 */
export function useWebSocket(url: string, token: string | null) {
  const clientRef = useRef<WebSocketClient | null>(null);
  const [status, setStatus] = useState<ConnectionStatus>('disconnected');

  useEffect(() => {
    if (!token) {
      return;
    }

    const client = new WebSocketClient(url, token);
    clientRef.current = client;

    // Subscribe to status changes
    const unsubscribeStatus = client.onStatusChange((newStatus) => {
      setStatus(newStatus);
    });

    // Connect
    client.connect();

    return () => {
      unsubscribeStatus();
      client.disconnect();
      clientRef.current = null;
    };
  }, [url, token]);

  const send = useCallback((data: unknown) => {
    clientRef.current?.send(data);
  }, []);

  return { status, send, client: clientRef.current };
}

/**
 * Hook to listen to specific WebSocket events.
 */
export function useWebSocketEvent<T = unknown>(
  client: WebSocketClient | null,
  eventType: EventType,
  handler: (data: T) => void
) {
  useEffect(() => {
    if (!client) {
      return;
    }

    const messageHandler: MessageHandler = (event: WebSocketEvent) => {
      if (event.type === eventType) {
        handler(event.data as T);
      }
    };

    const unsubscribe = client.onMessage(messageHandler);

    return unsubscribe;
  }, [client, eventType, handler]);
}

/**
 * Hook for dashboard stats updates.
 */
export function useDashboardStats(token: string | null) {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  // Fetch initial stats
  useEffect(() => {
    if (!token) {
      return;
    }

    const fetchStats = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${API_BASE_URL}/admin/dashboard/stats`, {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch dashboard stats');
        }

        const data = await response.json();
        setStats(data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, [token, API_BASE_URL]);

  // Subscribe to WebSocket updates
  const wsUrl = API_BASE_URL.replace('http://', 'ws://').replace('https://', 'wss://');
  const { client } = useWebSocket(`${wsUrl}/admin/ws`, token);

  useWebSocketEvent(client, 'dashboard_stats_updated', (data: DashboardStats) => {
    setStats(data);
  });

  return { stats, loading, error };
}

/**
 * Hook for products updates via WebSocket.
 */
export function useProducts(token: string | null) {
  const [products, setProducts] = useState<Product[]>([]);
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const wsUrl = API_BASE_URL.replace('http://', 'ws://').replace('https://', 'wss://');
  const { client } = useWebSocket(`${wsUrl}/admin/ws`, token);

  useWebSocketEvent(client, 'product_scraped', (data: { product_id: number }) => {
    // Refresh products list when new product is scraped
    // In a real implementation, you'd fetch the new product or update the list
  });

  useWebSocketEvent(client, 'score_calculated', (data: { product_id: number; score: number }) => {
    // Update product score when calculated
    setProducts((prev) =>
      prev.map((p) =>
        p.id === data.product_id ? { ...p, score: data.score, scored: true } : p
      )
    );
  });

  return { products, setProducts };
}

/**
 * Hook for campaigns updates via WebSocket.
 */
export function useCampaigns(token: string | null) {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const wsUrl = API_BASE_URL.replace('http://', 'ws://').replace('https://', 'wss://');
  const { client } = useWebSocket(`${wsUrl}/admin/ws`, token);

  useWebSocketEvent(client, 'campaign_status_changed', (data: { campaign_id: number; old_status: string; new_status: string }) => {
    setCampaigns((prev) =>
      prev.map((c) =>
        c.id === data.campaign_id ? { ...c, status: data.new_status as 'paused' | 'active' | 'completed' } : c
      )
    );
  });

  return { campaigns, setCampaigns };
}

/**
 * Hook for action status updates via WebSocket.
 */
export function useActionStatus(token: string | null) {
  const [scrapingStatus, setScrapingStatus] = useState<{ status: string; progress: number; ads_scraped: number } | null>(null);
  const [scoringStatus, setScoringStatus] = useState<{ status: string; progress: number; products_scored: number } | null>(null);
  const [creativeStatus, setCreativeStatus] = useState<{ product_id: number; status: string; progress: number } | null>(null);

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const wsUrl = API_BASE_URL.replace('http://', 'ws://').replace('https://', 'wss://');
  const { client } = useWebSocket(`${wsUrl}/admin/ws`, token);

  useWebSocketEvent(client, 'scraping_progress', (data: { status: string; progress: number; ads_scraped: number }) => {
    setScrapingStatus(data);
  });

  useWebSocketEvent(client, 'scraping_completed', (data: { ads_scraped: number }) => {
    setScrapingStatus({ status: 'completed', progress: 100, ads_scraped: data.ads_scraped });
  });

  useWebSocketEvent(client, 'scraping_failed', (data: { error: string }) => {
    setScrapingStatus({ status: 'failed', progress: 0, ads_scraped: 0 });
  });

  useWebSocketEvent(client, 'scoring_progress', (data: { status: string; progress: number; products_scored: number }) => {
    setScoringStatus(data);
  });

  useWebSocketEvent(client, 'scoring_completed', (data: { products_scored: number }) => {
    setScoringStatus({ status: 'completed', progress: 100, products_scored: data.products_scored });
  });

  useWebSocketEvent(client, 'scoring_failed', (data: { error: string }) => {
    setScoringStatus({ status: 'failed', progress: 0, products_scored: 0 });
  });

  useWebSocketEvent(client, 'creative_progress', (data: { product_id: number; status: string; progress: number }) => {
    setCreativeStatus(data);
  });

  useWebSocketEvent(client, 'creative_completed', (data: { product_id: number }) => {
    setCreativeStatus({ ...data, status: 'completed', progress: 100 });
  });

  useWebSocketEvent(client, 'creative_failed', (data: { product_id: number; error: string }) => {
    setCreativeStatus({ ...data, status: 'failed', progress: 0 });
  });

  return { scrapingStatus, scoringStatus, creativeStatus };
}

/**
 * Hook for orders updates via WebSocket.
 */
export function useOrders(token: string | null) {
  const [orders, setOrders] = useState<Order[]>([]);
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const wsUrl = API_BASE_URL.replace('http://', 'ws://').replace('https://', 'wss://');
  const { client } = useWebSocket(`${wsUrl}/admin/ws`, token);

  useWebSocketEvent(client, 'order_created', (data: { order_id: number; product_id: number; status: string }) => {
    // In a real implementation, you'd fetch the new order or add it to the list
  });

  useWebSocketEvent(client, 'order_status_changed', (data: { order_id: number; old_status: string; new_status: string }) => {
    setOrders((prev) =>
      prev.map((o) =>
        o.id === data.order_id ? { ...o, status: data.new_status as any } : o
      )
    );
  });

  return { orders, setOrders };
}
