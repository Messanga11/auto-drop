from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db, engine
from app.cache import get_redis
from typing import Dict, Any
import logging

router = APIRouter(prefix="/health", tags=["health"])
logger = logging.getLogger(__name__)


@router.get("", response_model=Dict[str, Any])
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "service": "dropshipping-api"
    }


@router.get("/detailed", response_model=Dict[str, Any])
async def detailed_health_check(db: AsyncSession = Depends(get_db)):
    """Detailed health check with database and cache status"""
    health_status = {
        "status": "healthy",
        "service": "dropshipping-api",
        "checks": {}
    }

    # Check database
    try:
        async with db.begin():
            await db.execute("SELECT 1")
        health_status["checks"]["database"] = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        health_status["checks"]["database"] = "unhealthy"
        health_status["status"] = "degraded"

    # Check Redis
    try:
        redis = await get_redis()
        await redis.ping()
        health_status["checks"]["redis"] = "healthy"
    except Exception as e:
        logger.error(f"Redis health check failed: {str(e)}")
        health_status["checks"]["redis"] = "unhealthy"
        health_status["status"] = "degraded"

    return health_status

