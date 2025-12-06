"""
Admin authentication routes.

Endpoints: /admin/auth/login, /admin/auth/logout, /admin/auth/me
"""

import logging
from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.admin import AdminUser
from app.services.admin.auth_service import AdminAuthService

# Import get_current_admin for /me endpoint
from app.middleware.admin_auth import get_current_admin

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["admin-auth"])


# Request/Response models
class LoginRequest(BaseModel):
    """Login request model."""

    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Login response model."""

    token: str
    expires_at: str
    admin: dict


class AdminUserResponse(BaseModel):
    """Admin user response model."""

    id: int
    email: str
    is_active: bool
    created_at: str
    last_login_at: Optional[str] = None

    class Config:
        from_attributes = True


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
    http_request: Request = None,
) -> LoginResponse:
    """
    Authenticate admin user and create session.

    Returns JWT token for subsequent requests.
    """
    # Authenticate user
    admin = await AdminAuthService.authenticate_user(
        db, request.email, request.password
    )

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )

    # Create JWT token
    token_data = {"sub": str(admin.id), "email": admin.email}
    token = AdminAuthService.create_access_token(
        data=token_data, expires_delta=timedelta(hours=24)
    )

    # Get client info
    ip_address = http_request.client.host if http_request else None
    user_agent = http_request.headers.get("user-agent") if http_request else None

    # Create session
    session = await AdminAuthService.create_session(
        db, admin, token, ip_address, user_agent
    )

    # Update last_login_at
    admin.last_login_at = session.created_at
    await db.commit()

    # Log action
    await AdminAuthService.log_action(
        db,
        admin.id,
        "login",
        "success",
        details={"ip_address": ip_address, "user_agent": user_agent},
    )

    return LoginResponse(
        token=token,
        expires_at=session.expires_at.isoformat(),
        admin={
            "id": admin.id,
            "email": admin.email,
            "is_active": admin.is_active,
            "created_at": admin.created_at.isoformat(),
            "last_login_at": admin.last_login_at.isoformat()
            if admin.last_login_at
            else None,
        },
    )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Logout admin user and revoke session.
    """
    from app.middleware.admin_auth import get_current_admin_optional

    # Get current admin if authenticated
    current_admin = await get_current_admin_optional(request, db)

    # Extract token from Authorization header
    authorization = request.headers.get("Authorization")
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
        await AdminAuthService.revoke_session(db, token)

        # Log action if admin was authenticated
        if current_admin:
            await AdminAuthService.log_action(
                db, current_admin.id, "logout", "success"
            )

    return {"message": "Logged out successfully"}


@router.get("/me", response_model=AdminUserResponse, status_code=status.HTTP_200_OK)
async def get_current_user(
    current_admin: AdminUser = Depends(get_current_admin),
) -> AdminUserResponse:
    """
    Get current authenticated admin user.
    """
    return AdminUserResponse(
        id=current_admin.id,
        email=current_admin.email,
        is_active=current_admin.is_active,
        created_at=current_admin.created_at.isoformat(),
        last_login_at=current_admin.last_login_at.isoformat()
        if current_admin.last_login_at
        else None,
    )

