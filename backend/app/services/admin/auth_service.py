"""
Admin authentication service.

Handles login, logout, token generation, and password hashing.
"""

import logging
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.admin import AdminAction, AdminSession, AdminUser

logger = logging.getLogger(__name__)

# JWT settings
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24  # 24 hours


class AdminAuthService:
    """Service for admin authentication."""

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against a hash.

        Args:
            plain_password: Plain text password
            hashed_password: Hashed password

        Returns:
            True if password matches, False otherwise
        """
        try:
            password_bytes = plain_password.encode('utf-8')
            if len(password_bytes) > 72:
                password_bytes = password_bytes[:72]
            return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))
        except Exception:
            return False

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Hash a password.

        Args:
            password: Plain text password

        Returns:
            Hashed password
        """
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create JWT access token.

        Args:
            data: Data to encode in token
            expires_delta: Optional expiration delta

        Returns:
            JWT token string
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        """
        Decode JWT token.

        Args:
            token: JWT token string

        Returns:
            Decoded token data or None if invalid
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None

    @staticmethod
    async def authenticate_user(
        db: AsyncSession, email: str, password: str
    ) -> Optional[AdminUser]:
        """
        Authenticate admin user.

        Args:
            db: Database session
            email: Admin email
            password: Plain text password

        Returns:
            AdminUser if authenticated, None otherwise
        """
        result = await db.execute(
            select(AdminUser).where(AdminUser.email == email)
        )
        admin = result.scalar_one_or_none()

        if not admin:
            return None

        if not admin.is_active:
            return None

        if not AdminAuthService.verify_password(password, admin.password_hash):
            return None

        return admin

    @staticmethod
    async def create_session(
        db: AsyncSession,
        admin: AdminUser,
        token: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AdminSession:
        """
        Create admin session.

        Args:
            db: Database session
            admin: Admin user
            token: JWT token
            ip_address: Optional IP address
            user_agent: Optional user agent

        Returns:
            Created AdminSession
        """
        expires_at = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)

        session = AdminSession(
            admin_id=admin.id,
            token=token,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        db.add(session)
        await db.commit()
        await db.refresh(session)

        return session

    @staticmethod
    async def get_session_by_token(
        db: AsyncSession, token: str
    ) -> Optional[AdminSession]:
        """
        Get session by token.

        Args:
            db: Database session
            token: JWT token

        Returns:
            AdminSession if found and valid, None otherwise
        """
        result = await db.execute(
            select(AdminSession)
            .where(AdminSession.token == token)
            .where(AdminSession.expires_at > datetime.utcnow())
        )
        session = result.scalar_one_or_none()

        if session:
            # Update last_used_at
            session.last_used_at = datetime.utcnow()
            await db.commit()

        return session

    @staticmethod
    async def revoke_session(db: AsyncSession, token: str) -> bool:
        """
        Revoke (delete) a session.

        Args:
            db: Database session
            token: JWT token

        Returns:
            True if session was revoked, False otherwise
        """
        result = await db.execute(
            select(AdminSession).where(AdminSession.token == token)
        )
        session = result.scalar_one_or_none()

        if session:
            await db.delete(session)
            await db.commit()
            return True

        return False

    @staticmethod
    async def log_action(
        db: AsyncSession,
        admin_id: int,
        action_type: str,
        result: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[int] = None,
        details: Optional[dict] = None,
    ) -> AdminAction:
        """
        Log admin action for audit trail.

        Args:
            db: Database session
            admin_id: Admin user ID
            action_type: Type of action
            result: Result (success, failure, partial)
            resource_type: Optional resource type
            resource_id: Optional resource ID
            details: Optional details dict

        Returns:
            Created AdminAction
        """
        import json

        action = AdminAction(
            admin_id=admin_id,
            action_type=action_type,
            resource_type=resource_type,
            resource_id=resource_id,
            result=result,
            details=json.dumps(details) if details else None,
        )

        db.add(action)
        await db.commit()
        await db.refresh(action)

        return action

