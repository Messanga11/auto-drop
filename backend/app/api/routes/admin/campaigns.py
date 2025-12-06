"""
Admin campaigns routes - Refactored to use centralized helpers.
"""

import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.admin_auth import get_current_admin
from app.models import Campaign
from app.models.admin import AdminUser
from app.services.admin.auth_service import AdminAuthService
from app.websocket.manager import websocket_manager
from app.utils.pagination import apply_pagination, get_total_count
from app.utils.response import format_list_response

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/campaigns", tags=["admin-campaigns"])


class CampaignResponse(BaseModel):
    """Campaign response model."""

    id: int
    product_id: int
    platform: str
    campaign_id: Optional[str]
    campaign_name: Optional[str]
    daily_budget: Optional[int]
    status: str
    created_at: str
    activated_at: Optional[str]

    class Config:
        from_attributes = True


class CampaignListResponse(BaseModel):
    """Campaign list response model."""

    campaigns: list[CampaignResponse]
    total: int


@router.get("", response_model=CampaignListResponse, status_code=status.HTTP_200_OK)
async def list_campaigns(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status"),
    platform: Optional[str] = Query(None, description="Filter by platform"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Page size"),
    current_admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> CampaignListResponse:
    """
    List campaigns with filters - Refactored to use helpers.
    """
    # Build base query
    query = select(Campaign)

    # Apply filters
    filter_conditions = []
    if status_filter:
        filter_conditions.append(Campaign.status == status_filter)
    if platform:
        filter_conditions.append(Campaign.platform == platform)
    if filter_conditions:
        query = query.where(and_(*filter_conditions))

    # Get total count using helper
    total = await get_total_count(query, Campaign, db, filter_conditions)

    # Apply pagination using helper
    query = apply_pagination(query, page, page_size)
    query = query.order_by(Campaign.created_at.desc())

    # Execute query
    result = await db.execute(query)
    campaigns = result.scalars().all()

    # Build response
    campaign_list = [
        CampaignResponse(
            id=c.id,
            product_id=c.product_id,
            platform=c.platform,
            campaign_id=c.campaign_id,
            campaign_name=c.campaign_name,
            daily_budget=c.daily_budget,
            status=c.status,
            created_at=c.created_at.isoformat() if c.created_at else "",
            activated_at=c.activated_at.isoformat() if c.activated_at else None,
        )
        for c in campaigns
    ]

    return CampaignListResponse(campaigns=campaign_list, total=total)


@router.post(
    "/{campaign_id}/activate",
    response_model=CampaignResponse,
    status_code=status.HTTP_200_OK,
)
async def activate_campaign(
    campaign_id: int = Path(..., description="Campaign ID"),
    current_admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> CampaignResponse:
    """
    Activate a campaign.
    """
    # Get campaign
    result = await db.execute(select(Campaign).where(Campaign.id == campaign_id))
    campaign = result.scalar_one_or_none()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found",
        )

    # Update status
    old_status = campaign.status
    campaign.status = "active"
    campaign.activated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(campaign)

    # Log action
    await AdminAuthService.log_action(
        db,
        current_admin.id,
        "campaign_activate",
        "success",
        resource_type="campaign",
        resource_id=campaign_id,
        details={"old_status": old_status, "new_status": "active"},
    )

    # Broadcast WebSocket event
    from app.websocket.events import create_event

    event = create_event(
        "campaign_status_changed",
        {
            "campaign_id": campaign_id,
            "old_status": old_status,
            "new_status": "active",
        },
    )
    await websocket_manager.broadcast(event)

    return CampaignResponse(
        id=campaign.id,
        product_id=campaign.product_id,
        platform=campaign.platform,
        campaign_id=campaign.campaign_id,
        campaign_name=campaign.campaign_name,
        daily_budget=campaign.daily_budget,
        status=campaign.status,
        created_at=campaign.created_at.isoformat() if campaign.created_at else "",
        activated_at=campaign.activated_at.isoformat() if campaign.activated_at else None,
    )


@router.post(
    "/{campaign_id}/deactivate",
    response_model=CampaignResponse,
    status_code=status.HTTP_200_OK,
)
async def deactivate_campaign(
    campaign_id: int = Path(..., description="Campaign ID"),
    current_admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> CampaignResponse:
    """
    Deactivate a campaign.
    """
    # Get campaign
    result = await db.execute(select(Campaign).where(Campaign.id == campaign_id))
    campaign = result.scalar_one_or_none()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found",
        )

    # Update status
    old_status = campaign.status
    campaign.status = "paused"
    await db.commit()
    await db.refresh(campaign)

    # Log action
    await AdminAuthService.log_action(
        db,
        current_admin.id,
        "campaign_deactivate",
        "success",
        resource_type="campaign",
        resource_id=campaign_id,
        details={"old_status": old_status, "new_status": "paused"},
    )

    # Broadcast WebSocket event
    from app.websocket.events import create_event

    event = create_event(
        "campaign_status_changed",
        {
            "campaign_id": campaign_id,
            "old_status": old_status,
            "new_status": "paused",
        },
    )
    await websocket_manager.broadcast(event)

    return CampaignResponse(
        id=campaign.id,
        product_id=campaign.product_id,
        platform=campaign.platform,
        campaign_id=campaign.campaign_id,
        campaign_name=campaign.campaign_name,
        daily_budget=campaign.daily_budget,
        status=campaign.status,
        created_at=campaign.created_at.isoformat() if campaign.created_at else "",
        activated_at=campaign.activated_at.isoformat() if campaign.activated_at else None,
    )
