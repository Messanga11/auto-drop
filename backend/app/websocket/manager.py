"""
WebSocket connection manager for admin real-time updates.

Manages active WebSocket connections, broadcasts events, and handles reconnection.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import WebSocket

from app.websocket.events import create_event

logger = logging.getLogger(__name__)


class WebSocketManager:
    """Manages WebSocket connections and event broadcasting."""

    def __init__(self):
        # Map: connection_id -> WebSocket
        self.active_connections: Dict[str, WebSocket] = {}
        # Map: connection_id -> admin_id
        self.connection_admin_map: Dict[str, int] = {}
        # Map: connection_id -> last_connection_time (for event replay)
        self.connection_times: Dict[str, datetime] = {}
        # Event history for replay (last 100 events)
        self.event_history: List[dict] = []
        self.max_history_size = 100

    async def connect(self, websocket: WebSocket, connection_id: str, admin_id: int) -> None:
        """
        Register a new WebSocket connection.

        Args:
            websocket: WebSocket connection
            connection_id: Unique connection identifier
            admin_id: Admin user ID
        """
        await websocket.accept()
        self.active_connections[connection_id] = websocket
        self.connection_admin_map[connection_id] = admin_id
        self.connection_times[connection_id] = datetime.utcnow()
        
        logger.info(f"WebSocket connected: {connection_id} (admin_id={admin_id})")
        
        # Send connection established event
        await self.send_to_connection(
            connection_id,
            create_event("connection_established", {"connection_id": connection_id}),
        )
        
        # Replay missed events
        await self.replay_missed_events(connection_id)

    async def disconnect(self, connection_id: str, websocket: Optional[WebSocket] = None) -> None:
        """
        Unregister a WebSocket connection.

        Args:
            connection_id: Connection identifier
        """
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
        if connection_id in self.connection_admin_map:
            del self.connection_admin_map[connection_id]
        if connection_id in self.connection_times:
            del self.connection_times[connection_id]
        
        logger.info(f"WebSocket disconnected: {connection_id}")

    async def send_to_connection(self, connection_id: str, event: dict) -> bool:
        """
        Send event to a specific connection.

        Args:
            connection_id: Connection identifier
            event: Event dictionary

        Returns:
            True if sent successfully, False otherwise
        """
        if connection_id not in self.active_connections:
            return False
        
        websocket = self.active_connections[connection_id]
        try:
            await websocket.send_json(event)
            return True
        except Exception as e:
            logger.error(f"Error sending to connection {connection_id}: {e}")
            await self.disconnect(connection_id)
            return False

    async def broadcast(self, event: dict, exclude_connection_id: Optional[str] = None) -> None:
        """
        Broadcast event to all connected clients.

        Optimized to reduce unnecessary broadcasts and handle errors gracefully.

        Args:
            event: Event dictionary
            exclude_connection_id: Optional connection ID to exclude from broadcast
        """
        # Add to event history for replay
        self.event_history.append(event)
        if len(self.event_history) > self.max_history_size:
            self.event_history.pop(0)
        
        # Batch send to all connections
        disconnected = []
        send_tasks = []
        
        for connection_id, websocket in self.active_connections.items():
            if connection_id == exclude_connection_id:
                continue
            
            # Create send task
            async def send_to_conn(conn_id: str, ws: WebSocket):
                try:
                    await ws.send_json(event)
                except Exception as e:
                    logger.error(f"Error broadcasting to {conn_id}: {e}")
                    disconnected.append(conn_id)
            
            send_tasks.append(send_to_conn(connection_id, websocket))
        
        # Execute all sends in parallel
        if send_tasks:
            import asyncio
            await asyncio.gather(*send_tasks, return_exceptions=True)
        
        # Clean up disconnected connections
        for connection_id in disconnected:
            await self.disconnect(connection_id)

    async def replay_missed_events(self, connection_id: str) -> None:
        """
        Replay events missed during disconnection.

        Args:
            connection_id: Connection identifier
        """
        if connection_id not in self.connection_times:
            return
        
        last_connection = self.connection_times[connection_id]
        
        # Replay all events since last connection
        for event in self.event_history:
            event_time = datetime.fromisoformat(event["timestamp"])
            if event_time > last_connection:
                await self.send_to_connection(connection_id, event)
        
        # Update connection time
        self.connection_times[connection_id] = datetime.utcnow()

    def get_connection_count(self) -> int:
        """Get number of active connections."""
        return len(self.active_connections)

    def get_admin_connections(self, admin_id: int) -> List[str]:
        """
        Get all connection IDs for a specific admin.

        Args:
            admin_id: Admin user ID

        Returns:
            List of connection IDs
        """
        return [
            conn_id
            for conn_id, aid in self.connection_admin_map.items()
            if aid == admin_id
        ]


# Global WebSocket manager instance
websocket_manager = WebSocketManager()

