"""
Dashboard service for admin application.

Provides statistics and metrics for the admin dashboard.
"""

import logging
from typing import Dict, List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import (
    Campaign,
    Creative,
    Order,
    ProductScore,
    ScrapedAd,
)

logger = logging.getLogger(__name__)


class DashboardService:
    """Service for dashboard statistics."""

    @staticmethod
    async def get_stats(db: AsyncSession) -> Dict:
        """
        Get dashboard statistics.

        Returns:
            Dictionary with dashboard stats:
            - total_products: Total number of scraped products
            - scored_products: Number of products with scores
            - top_5_products: Top 5 products by score
            - active_campaigns: Number of active campaigns
            - pending_orders: Number of pending orders
        """
        stats = {}

        # Total products (scraped ads)
        result = await db.execute(
            select(func.count(ScrapedAd.id))
        )
        stats["total_products"] = result.scalar() or 0

        # Scored products
        result = await db.execute(
            select(func.count(ProductScore.id))
        )
        stats["scored_products"] = result.scalar() or 0

        # Top 5 products by score
        result = await db.execute(
            select(ProductScore)
            .order_by(ProductScore.score.desc())
            .limit(5)
        )
        top_products = result.scalars().all()
        stats["top_5_products"] = [
            {
                "id": p.id,
                "product_id": p.ad_id,
                "total_score": float(p.score) if p.score else 0.0,
                "engagement_score": float(p.engagement_score) if p.engagement_score else 0.0,
                "calculated_at": p.calculated_at.isoformat() if p.calculated_at else None,
            }
            for p in top_products
        ]

        # Active campaigns
        result = await db.execute(
            select(func.count(Campaign.id))
            .where(Campaign.status == "active")
        )
        stats["active_campaigns"] = result.scalar() or 0

        # Pending orders
        result = await db.execute(
            select(func.count(Order.id))
            .where(Order.status == "pending")
        )
        stats["pending_orders"] = result.scalar() or 0

        # Additional stats
        # Total campaigns
        result = await db.execute(
            select(func.count(Campaign.id))
        )
        stats["total_campaigns"] = result.scalar() or 0

        # Total orders
        result = await db.execute(
            select(func.count(Order.id))
        )
        stats["total_orders"] = result.scalar() or 0

        # Total creatives
        result = await db.execute(
            select(func.count(Creative.id))
        )
        stats["total_creatives"] = result.scalar() or 0

        return stats

