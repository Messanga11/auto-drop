"""
Admin action service for triggering system actions.

Handles scraping, scoring, and creative generation triggers.
"""

import logging
from typing import Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.admin import AdminUser
from app.services.admin.auth_service import AdminAuthService

logger = logging.getLogger(__name__)


class ActionService:
    """Service for triggering system actions."""

    @staticmethod
    async def trigger_scraping(
        db: AsyncSession,
        admin: AdminUser,
        platform: Optional[str] = None,
    ) -> Dict:
        """
        Trigger scraping action.

        Args:
            db: Database session
            admin: Admin user triggering the action
            platform: Optional platform filter (facebook, tiktok)

        Returns:
            Action status dictionary
        """
        # Import here to avoid circular dependencies
        from app.services.scraping_service import ScrapingService

        # Log action
        await AdminAuthService.log_action(
            db,
            admin.id,
            "scraping_start",
            "success",
            resource_type="scraping",
            details={"platform": platform},
        )

        # Trigger scraping (this would typically be async/background task)
        # For now, we'll return a status indicating the action was triggered
        try:
            # In a real implementation, this would start a background task
            # For now, we'll just return a status
            return {
                "status": "started",
                "message": "Scraping started",
                "platform": platform,
            }
        except Exception as e:
            logger.error(f"Error triggering scraping: {e}")
            await AdminAuthService.log_action(
                db,
                admin.id,
                "scraping_start",
                "failure",
                resource_type="scraping",
                details={"error": str(e)},
            )
            raise

    @staticmethod
    async def get_scraping_status(db: AsyncSession) -> Dict:
        """
        Get scraping status.

        Returns:
            Scraping status dictionary
        """
        # In a real implementation, this would check the status of the scraping task
        # For now, we'll return a mock status
        return {
            "status": "idle",  # idle, running, completed, failed
            "progress": 0,
            "ads_scraped": 0,
        }

    @staticmethod
    async def trigger_scoring(
        db: AsyncSession,
        admin: AdminUser,
    ) -> Dict:
        """
        Trigger scoring calculation.

        Args:
            db: Database session
            admin: Admin user triggering the action

        Returns:
            Action status dictionary
        """
        from app.services.scoring_service import ScoringService

        # Log action
        await AdminAuthService.log_action(
            db,
            admin.id,
            "scoring_calculate",
            "success",
            resource_type="scoring",
        )

        try:
            # In a real implementation, this would start a background task
            return {
                "status": "started",
                "message": "Scoring calculation started",
            }
        except Exception as e:
            logger.error(f"Error triggering scoring: {e}")
            await AdminAuthService.log_action(
                db,
                admin.id,
                "scoring_calculate",
                "failure",
                resource_type="scoring",
                details={"error": str(e)},
            )
            raise

    @staticmethod
    async def trigger_creative_generation(
        db: AsyncSession,
        admin: AdminUser,
        product_id: int,
    ) -> Dict:
        """
        Trigger creative generation for a product.

        Args:
            db: Database session
            admin: Admin user triggering the action
            product_id: Product ID to generate creatives for

        Returns:
            Action status dictionary
        """
        from app.services.creatify_service import CreatifyService
        from app.models import ScrapedAd
        from sqlalchemy import select

        # Log action
        await AdminAuthService.log_action(
            db,
            admin.id,
            "creative_generate",
            "started",
            resource_type="creative",
            resource_id=product_id,
            details={"product_id": product_id},
        )

        try:
            # Verify product exists
            result = await db.execute(select(ScrapedAd).where(ScrapedAd.id == product_id))
            product = result.scalar_one_or_none()
            
            if not product:
                raise ValueError(f"Product {product_id} not found")
            
            # In a real implementation, this would start a background task
            # For now, we just return success
            return {
                "status": "started",
                "message": "Creative generation started",
                "product_id": product_id,
            }
        except Exception as e:
            logger.error(f"Error triggering creative generation: {e}")
            await AdminAuthService.log_action(
                db,
                admin.id,
                "creative_generate",
                "failure",
                resource_type="creative",
                resource_id=product_id,
                details={"error": str(e)},
            )
            raise

