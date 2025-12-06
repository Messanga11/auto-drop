/**
 * WebSocket client with automatic reconnection for admin real-time updates.
 * 
 * Features:
 * - Automatic reconnection with exponential backoff (500ms → 60s, unlimited attempts)
 * - Event replay on reconnection
 * - Connection status management
 */

import { EventType, WebSocketEvent } from './events';

export type ConnectionStatus = 'disconnected' | 'connecting' | 'connected' | 'reconnecting';

export type MessageHandler = (event: WebSocketEvent) => void;
export type StatusChangeHandler = (status: ConnectionStatus) => void;

export class WebSocketClient {
  private ws: WebSocket | null = null;
  private url: string;
  private token: string;
  private status: ConnectionStatus = 'disconnected';
  private reconnectAttempts = 0;
  private maxReconnectDelay = 60000; // 60 seconds
  private initialReconnectDelay = 500; // 500ms
  private reconnectTimeout: NodeJS.Timeout | null = null;
  private messageHandlers: Set<MessageHandler> = new Set();
  private statusChangeHandlers: Set<StatusChangeHandler> = new Set();
  private missedEvents: WebSocketEvent[] = [];
  private lastConnectionTime: Date | null = null;
  private maxRetries = Infinity; // Unlimited retries
  private retryCount = 0;

  constructor(url: string, token: string) {
    this.url = url;
    this.token = token;
  }

  /**
   * Connect to WebSocket server.
   */
  connect(): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      return; // Already connected
    }

    this.setStatus('connecting');
    const wsUrl = `${this.url}?token=${encodeURIComponent(this.token)}`;
    
    try {
      this.ws = new WebSocket(wsUrl);
      this.setupEventHandlers();
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      console.error('WebSocket connection error:', errorMessage);
      this.scheduleReconnect();
    }
  }

  /**
   * Disconnect from WebSocket server.
   */
  disconnect(): void {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = null;
    }

    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }

    this.setStatus('disconnected');
    this.reconnectAttempts = 0;
  }

  /**
   * Send message to WebSocket server.
   */
  send(data: unknown): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      try {
        this.ws.send(JSON.stringify(data));
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown send error';
        console.error('Error sending WebSocket message:', errorMessage);
      }
    } else {
      // Only warn if we're not in a reconnecting state (to avoid spam)
      if (this.status !== 'reconnecting') {
        console.warn('WebSocket is not connected, cannot send message', {
          readyState: this.ws?.readyState,
          status: this.status,
        });
      }
    }
  }

  /**
   * Register message handler.
   */
  onMessage(handler: MessageHandler): () => void {
    this.messageHandlers.add(handler);
    return () => this.messageHandlers.delete(handler);
  }

  /**
   * Register status change handler.
   */
  onStatusChange(handler: StatusChangeHandler): () => void {
    this.statusChangeHandlers.add(handler);
    return () => this.statusChangeHandlers.delete(handler);
  }

  /**
   * Get current connection status.
   */
  getStatus(): ConnectionStatus {
    return this.status;
  }

  private setupEventHandlers(): void {
    if (!this.ws) return;

    this.ws.onopen = () => {
      console.log('WebSocket connected successfully');
      this.setStatus('connected');
      this.reconnectAttempts = 0;
      this.retryCount = 0;
      this.lastConnectionTime = new Date();
      
      // Request missed events replay
      try {
        this.send({ type: 'reconnect_requested', data: {} });
      } catch (error) {
        // Ignore send errors on initial connection
      }
    };

    this.ws.onmessage = (event) => {
      try {
        const message: WebSocketEvent = JSON.parse(event.data);
        
        // Handle connection established event
        if (message.type === 'connection_established') {
          // Server will replay missed events automatically
          // Clear any local missed events as server handles replay
          this.missedEvents = [];
        }
        
        // Store events while disconnected for replay
        if (this.status === 'disconnected' || this.status === 'reconnecting') {
          this.missedEvents.push(message);
        }
        
        // Notify all handlers
        this.messageHandlers.forEach(handler => {
          try {
            handler(message);
          } catch (handlerError) {
            console.error('Error in WebSocket message handler:', handlerError);
          }
        });
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown parsing error';
        console.error('Error parsing WebSocket message:', errorMessage, event.data);
      }
    };

    this.ws.onerror = () => {
      // WebSocket error events don't provide much detail - the actual error
      // information is usually in the onclose event with the close code.
      // The error object is often empty {}, so we don't log it to avoid noise.
      // Error details will be available in onclose event with the close code.
      // We silently handle errors here - they will be logged in onclose if meaningful
    };

    this.ws.onclose = (event) => {
      // Log close event with details (only for non-normal closures)
      if (event.code !== 1000) {
        // Only log non-normal closures
        const closeInfo: Record<string, any> = {
          code: event.code,
          wasClean: event.wasClean,
        };
        if (event.reason) {
          closeInfo.reason = event.reason;
        }
        console.log('WebSocket closed:', closeInfo);
      }
      
      this.ws = null;
      this.setStatus('disconnected');
      
      // Don't reconnect if closed normally or due to authentication failure
      if (event.code === 1000) {
        // Normal closure - no action needed
        return;
      }
      
      if (event.code === 1008) {
        // Policy violation (e.g., authentication failure)
        console.warn('WebSocket closed due to policy violation (likely authentication failure)');
        return;
      }
      
      // Schedule reconnection with retry logic
      if (this.retryCount < this.maxRetries) {
        this.scheduleReconnect();
      } else {
        console.error('Max retries reached, stopping reconnection attempts');
      }
    };
  }

  private setStatus(status: ConnectionStatus): void {
    if (this.status !== status) {
      this.status = status;
      this.statusChangeHandlers.forEach(handler => handler(status));
    }
  }

  private scheduleReconnect(): void {
    if (this.reconnectTimeout) {
      return; // Already scheduled
    }

    // Calculate delay with exponential backoff
    const delay = Math.min(
      this.initialReconnectDelay * Math.pow(2, this.reconnectAttempts),
      this.maxReconnectDelay
    );

    this.setStatus('reconnecting');
    this.reconnectAttempts++;
    this.retryCount++;

    this.reconnectTimeout = setTimeout(() => {
      this.reconnectTimeout = null;
      this.connect();
    }, delay);
  }

  private replayMissedEvents(): void {
    // Replay missed events that weren't handled by server
    if (this.missedEvents.length > 0) {
      console.log(`Replaying ${this.missedEvents.length} missed events`);
      this.missedEvents.forEach(event => {
        this.messageHandlers.forEach(handler => handler(event));
      });
      this.missedEvents = [];
    }
  }
}
