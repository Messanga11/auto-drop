"""
Admin products routes - Refactored to use centralized helpers.
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.admin_auth import get_current_admin
from app.models import ProductScore, ScrapedAd
from app.models.admin import AdminUser
from app.utils.pagination import apply_pagination, get_total_count
from app.utils.response import format_list_response

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["admin-products"])


class ProductResponse(BaseModel):
    """Product response model."""

    id: int
    platform: str
    ad_id: Optional[str]
    page_name: Optional[str]
    advertiser_name: Optional[str]
    caption: Optional[str]
    likes: int
    comments: int
    shares: int
    views: int
    scraped_at: str
    scored: bool
    selected_for_campaign: bool
    score: Optional[float] = None
    engagement_rate: Optional[float] = None

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    """Product list response model."""

    products: list[ProductResponse]
    total: int
    page: int
    page_size: int


@router.get("", response_model=ProductListResponse, status_code=status.HTTP_200_OK)
async def list_products(
    platform: Optional[str] = Query(None, description="Filter by platform"),
    scored: Optional[bool] = Query(None, description="Filter by scored status"),
    min_score: Optional[float] = Query(None, description="Minimum score"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Page size"),
    current_admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> ProductListResponse:
    """
    List products with filters and pagination - Refactored to use helpers.
    """
    # Build base query
    query = select(ScrapedAd)

    # Apply filters
    filter_conditions = []

    if platform:
        filter_conditions.append(ScrapedAd.platform == platform)

    if scored is not None:
        filter_conditions.append(ScrapedAd.scored == scored)

    # Apply filters to query
    if filter_conditions:
        query = query.where(and_(*filter_conditions))

    # Get total count using helper
    total = await get_total_count(query, ScrapedAd, db, filter_conditions)

    # Apply pagination using helper
    query = apply_pagination(query, page, page_size)
    query = query.order_by(ScrapedAd.scraped_at.desc())

    # Execute query
    result = await db.execute(query)
    ads = result.scalars().all()

    # Get scores for products
    product_ids = [ad.id for ad in ads]
    if product_ids:
        scores_query = select(ProductScore).where(
            ProductScore.ad_id.in_(product_ids)
        )
        scores_result = await db.execute(scores_query)
        scores = {
            score.ad_id: score
            for score in scores_result.scalars().all()
        }
    else:
        scores = {}

    # Build response
    products = []
    for ad in ads:
        score = scores.get(ad.id)
        products.append(
            ProductResponse(
                id=ad.id,
                platform=ad.platform,
                ad_id=ad.ad_id,
                page_name=ad.page_name,
                advertiser_name=ad.advertiser_name,
                caption=ad.caption,
                likes=ad.likes or 0,
                comments=ad.comments or 0,
                shares=ad.shares or 0,
                views=ad.views or 0,
                scraped_at=ad.scraped_at.isoformat()
                if ad.scraped_at
                else "",
                scored=ad.scored or False,
                selected_for_campaign=ad.selected_for_campaign or False,
                score=float(score.score)
                if score and score.score
                else None,
                engagement_rate=float(score.engagement_score)
                if score and score.engagement_score
                else None,
            )
        )

    # Format response using helper
    response_data = format_list_response(products, total, page, page_size)

    return ProductListResponse(
        products=response_data["items"],
        total=response_data["total"],
        page=response_data["page"],
        page_size=response_data["page_size"],
    )
