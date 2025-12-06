"""
Admin actions routes.

Endpoints: /admin/actions/*
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.admin_auth import get_current_admin
from app.models.admin import AdminUser
from app.services.admin.action_service import ActionService
from app.websocket.manager import websocket_manager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/actions", tags=["admin-actions"])


class ActionResponse(BaseModel):
    """Action response model."""

    status: str
    message: str
    platform: Optional[str] = None
    product_id: Optional[int] = None


class ScrapingStatusResponse(BaseModel):
    """Scraping status response model."""

    status: str  # idle, running, completed, failed
    progress: int  # 0-100
    ads_scraped: int


@router.post(
    "/scraping/start",
    response_model=ActionResponse,
    status_code=status.HTTP_200_OK,
)
async def start_scraping(
    platform: Optional[str] = Query(None, description="Platform filter"),
    current_admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> ActionResponse:
    """
    Start scraping action.
    """
    result = await ActionService.trigger_scraping(db, current_admin, platform)

    # Broadcast WebSocket event
    from app.websocket.events import create_event

    event = create_event(
        "scraping_progress",
        {
            "status": "started",
            "progress": 0,
            "ads_scraped": 0,
        },
    )
    await websocket_manager.broadcast(event)

    return ActionResponse(**result)


@router.get(
    "/scraping/status",
    response_model=ScrapingStatusResponse,
    status_code=status.HTTP_200_OK,
)
async def get_scraping_status(
    current_admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> ScrapingStatusResponse:
    """
    Get scraping status.
    """
    status_data = await ActionService.get_scraping_status(db)
    return ScrapingStatusResponse(**status_data)


@router.post(
    "/scoring/calculate",
    response_model=ActionResponse,
    status_code=status.HTTP_200_OK,
)
async def calculate_scoring(
    current_admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> ActionResponse:
    """
    Trigger scoring calculation.
    """
    result = await ActionService.trigger_scoring(db, current_admin)

    # Broadcast WebSocket event
    from app.websocket.events import create_event

    event = create_event(
        "scoring_progress",
        {
            "status": "started",
            "progress": 0,
            "products_scored": 0,
        },
    )
    await websocket_manager.broadcast(event)

    return ActionResponse(**result)


@router.post(
    "/creatives/generate/{product_id}",
    response_model=ActionResponse,
    status_code=status.HTTP_200_OK,
)
async def generate_creatives(
    product_id: int = Path(..., description="Product ID"),
    current_admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> ActionResponse:
    """
    Trigger creative generation for a product.
    """
    result = await ActionService.trigger_creative_generation(
        db, current_admin, product_id
    )

    # Broadcast WebSocket event
    from app.websocket.events import create_event

    event = create_event(
        "creative_progress",
        {
            "product_id": product_id,
            "status": "started",
            "progress": 0,
        },
    )
    await websocket_manager.broadcast(event)

    return ActionResponse(**result)

