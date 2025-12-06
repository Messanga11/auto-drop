"""
Script to seed default admin user.

This script creates a default admin user with email 'admin@dropshipping.com'
and password from environment variable ADMIN_DEFAULT_PASSWORD (default: 'admin123').
"""

import asyncio
import os
from datetime import datetime, timedelta

import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import AsyncSessionLocal
from app.models.admin import AdminUser


async def seed_admin_user() -> None:
    """
    Create default admin user if it doesn't exist.
    
    Email: admin@dropshipping.com
    Password: From ADMIN_DEFAULT_PASSWORD env var (default: admin123)
    """
    async with AsyncSessionLocal() as session:
        # Check if admin user already exists
        result = await session.execute(select(AdminUser).where(AdminUser.email == "admin@dropshipping.com"))
        existing_admin = result.scalar_one_or_none()
        
        if existing_admin:
            print("✅ Admin user already exists, skipping seed.")
            return
        
        # Get password from environment or use default
        default_password = os.getenv("ADMIN_DEFAULT_PASSWORD", "admin123")
        # Hash password directly with bcrypt (avoiding passlib compatibility issues)
        password_bytes = default_password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
        
        # Create admin user
        admin_user = AdminUser(
            email="admin@dropshipping.com",
            password_hash=password_hash,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        
        session.add(admin_user)
        await session.commit()
        
        print(f"✅ Default admin user created successfully!")
        print(f"   Email: admin@dropshipping.com")
        print(f"   Password: {default_password}")
        print(f"   ⚠️  Please change the default password in production!")


if __name__ == "__main__":
    asyncio.run(seed_admin_user())

