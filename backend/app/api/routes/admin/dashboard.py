"""
Admin dashboard routes.

Endpoints: /admin/dashboard/stats
"""

import logging

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.admin_auth import get_current_admin
from app.models.admin import AdminUser
from app.services.admin.dashboard_service import DashboardService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dashboard", tags=["admin-dashboard"])


class DashboardStatsResponse(BaseModel):
    """Dashboard statistics response model."""

    total_products: int
    scored_products: int
    top_5_products: list
    active_campaigns: int
    pending_orders: int
    total_campaigns: int
    total_orders: int
    total_creatives: int


@router.get(
    "/stats",
    response_model=DashboardStatsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_dashboard_stats(
    current_admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> DashboardStatsResponse:
    """
    Get dashboard statistics.

    Returns statistics about products, campaigns, orders, and creatives.
    """
    stats = await DashboardService.get_stats(db)

    return DashboardStatsResponse(**stats)

