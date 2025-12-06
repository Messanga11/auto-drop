"""
Admin creatives routes - Refactored to use centralized helpers.
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.admin_auth import get_current_admin
from app.models import Creative
from app.models.admin import AdminUser
from app.utils.pagination import apply_pagination, get_total_count
from app.utils.response import format_list_response

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/creatives", tags=["admin-creatives"])


class CreativeResponse(BaseModel):
    """Creative response model."""

    id: int
    product_id: int
    video_id: Optional[str]
    video_type: Optional[str]
    status: Optional[str]
    download_url: Optional[str]
    created_at: str
    completed_at: Optional[str]

    class Config:
        from_attributes = True


class CreativeListResponse(BaseModel):
    """Creative list response model."""

    creatives: list[CreativeResponse]
    total: int


@router.get("", response_model=CreativeListResponse, status_code=status.HTTP_200_OK)
async def list_creatives(
    product_id: Optional[int] = Query(None, description="Filter by product ID"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Page size"),
    current_admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> CreativeListResponse:
    """
    List creatives with filters - Refactored to use helpers.
    """
    # Build base query
    query = select(Creative)

    # Apply filters
    filter_conditions = []
    if product_id:
        filter_conditions.append(Creative.product_id == product_id)
    if status_filter:
        filter_conditions.append(Creative.status == status_filter)
    if filter_conditions:
        query = query.where(and_(*filter_conditions))

    # Get total count using helper
    total = await get_total_count(query, Creative, db, filter_conditions)

    # Apply pagination using helper
    query = apply_pagination(query, page, page_size)
    query = query.order_by(Creative.created_at.desc())

    # Execute query
    result = await db.execute(query)
    creatives = result.scalars().all()

    # Build response
    creative_list = [
        CreativeResponse(
            id=c.id,
            product_id=c.product_id,
            video_id=c.video_id,
            video_type=c.video_type,
            status=c.status,
            download_url=c.download_url,
            created_at=c.created_at.isoformat() if c.created_at else "",
            completed_at=c.completed_at.isoformat() if c.completed_at else None,
        )
        for c in creatives
    ]

    return CreativeListResponse(creatives=creative_list, total=total)
