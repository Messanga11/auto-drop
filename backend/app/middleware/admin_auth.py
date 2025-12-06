"""
Admin authentication middleware.

Extracts and validates JWT token from Authorization header.
"""

import logging
from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.admin import AdminSession, AdminUser
from app.services.admin.auth_service import AdminAuthService

logger = logging.getLogger(__name__)

security = HTTPBearer()


async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> AdminUser:
    """
    Get current authenticated admin user from JWT token.

    This dependency extracts the token from the Authorization header,
    validates it, and returns the AdminUser.

    Args:
        credentials: HTTP Bearer credentials
        db: Database session

    Returns:
        AdminUser if authenticated

    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials

    # Decode token
    payload = AdminAuthService.decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get admin ID from token
    admin_id = payload.get("sub")
    if not admin_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify session exists and is valid
    session = await AdminAuthService.get_session_by_token(db, token)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get admin user
    result = await db.execute(
        select(AdminUser).where(AdminUser.id == int(admin_id))
    )
    admin = result.scalar_one_or_none()

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin user not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )

    return admin


async def get_current_admin_optional(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> Optional[AdminUser]:
    """
    Get current authenticated admin user (optional).

    Returns None if not authenticated instead of raising exception.
    Useful for endpoints that work with or without authentication.

    Args:
        request: FastAPI request
        db: Database session

    Returns:
        AdminUser if authenticated, None otherwise
    """
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        return None

    token = authorization.replace("Bearer ", "")

    try:
        payload = AdminAuthService.decode_token(token)
        if not payload:
            return None

        admin_id = payload.get("sub")
        if not admin_id:
            return None

        session = await AdminAuthService.get_session_by_token(db, token)
        if not session:
            return None

        result = await db.execute(
            select(AdminUser).where(AdminUser.id == int(admin_id))
        )
        admin = result.scalar_one_or_none()

        if admin and admin.is_active:
            return admin

        return None
    except Exception as e:
        logger.warning(f"Error in optional auth: {e}")
        return None

