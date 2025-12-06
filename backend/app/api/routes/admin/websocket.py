"""
Admin WebSocket routes.

WebSocket endpoint: /admin/ws?token=...
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.admin_auth import get_current_admin_optional
from app.models.admin import AdminUser
from app.websocket.events import EventType, WebSocketEvent, create_event
from app.websocket.manager import websocket_manager

logger = logging.getLogger(__name__)

router = APIRouter(tags=["admin-websocket"])


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """
    WebSocket endpoint for admin real-time updates.

    Authentication via token query parameter.
    """
    # Authenticate admin user
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # Create a request-like object for authentication
    class FakeRequest:
        def __init__(self, token: str):
            self.headers = {"Authorization": f"Bearer {token}"}

    fake_request = FakeRequest(token)
    admin = await get_current_admin_optional(fake_request, db)

    if not admin:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # Accept WebSocket connection
    connection_id = f"admin_{admin.id}_{id(websocket)}"
    await websocket_manager.connect(websocket, connection_id, admin.id)

    try:
        # Send welcome message
        welcome_event = create_event(
            "connection_established",
            {"message": "Connected to admin WebSocket", "admin_id": admin.id},
        )
        await websocket.send_json(welcome_event)

        # Keep connection alive and handle messages
        while True:
            data = await websocket.receive_text()
            # Echo back for ping/pong or handle client messages
            if data == "ping":
                await websocket.send_text("pong")

    except WebSocketDisconnect:
        connection_id = f"admin_{admin.id}_{id(websocket)}"
        await websocket_manager.disconnect(connection_id)
        logger.info(f"Admin {admin.id} disconnected from WebSocket")
    except Exception as e:
        logger.error(f"WebSocket error for admin {admin.id}: {e}")
        connection_id = f"admin_{admin.id}_{id(websocket)}"
        await websocket_manager.disconnect(connection_id)
        await websocket.close()

