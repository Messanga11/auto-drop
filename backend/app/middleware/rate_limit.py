from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.cache import get_redis
import time
import logging

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute

    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks and docs
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get client IP
        client_ip = request.client.host if request.client else "unknown"

        try:
            redis = await get_redis()
            key = f"rate_limit:{client_ip}"
            current = await redis.get(key)

            if current and int(current) >= self.requests_per_minute:
                logger.warning(f"Rate limit exceeded for {client_ip}")
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests. Please try again later."
                )

            # Increment counter
            pipe = redis.pipeline()
            pipe.incr(key)
            pipe.expire(key, 60)  # Reset after 1 minute
            await pipe.execute()

        except Exception as e:
            logger.error(f"Rate limit error: {str(e)}")
            # Continue if Redis is unavailable

        return await call_next(request)

