"""
Admin models for Admin Dashboard Application.

Models: AdminUser, AdminSession, AdminAction
"""

from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AdminUser(Base):
    """Compte administrateur avec authentification."""

    __tablename__ = "admin_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    sessions: Mapped[list["AdminSession"]] = relationship("AdminSession", back_populates="admin", cascade="all, delete-orphan")
    actions: Mapped[list["AdminAction"]] = relationship("AdminAction", back_populates="admin", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<AdminUser(id={self.id}, email={self.email}, is_active={self.is_active})>"


class AdminSession(Base):
    """Session d'authentification active pour un administrateur."""

    __tablename__ = "admin_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    admin_id: Mapped[int] = mapped_column(Integer, ForeignKey("admin_users.id", ondelete="CASCADE"), nullable=False, index=True)
    token: Mapped[str] = mapped_column(String(512), unique=True, nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)  # IPv4 or IPv6
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_used_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    admin: Mapped["AdminUser"] = relationship("AdminUser", back_populates="sessions")

    def __repr__(self) -> str:
        return f"<AdminSession(id={self.id}, admin_id={self.admin_id}, expires_at={self.expires_at})>"


class AdminAction(Base):
    """Action administrative effectuée par un administrateur (audit trail)."""

    __tablename__ = "admin_actions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    admin_id: Mapped[int] = mapped_column(Integer, ForeignKey("admin_users.id", ondelete="CASCADE"), nullable=False, index=True)
    action_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    resource_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    resource_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    result: Mapped[str] = mapped_column(String(20), nullable=False)  # "success", "failure", "partial"
    details: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON stored as text (SQLite compatible)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    # Relationships
    admin: Mapped["AdminUser"] = relationship("AdminUser", back_populates="actions")

    def __repr__(self) -> str:
        return f"<AdminAction(id={self.id}, admin_id={self.admin_id}, action_type={self.action_type}, result={self.result})>"

