"""
Admin orders routes - Refactored to use centralized helpers.
"""

import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import BaseModel
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.admin_auth import get_current_admin
from app.models import Order
from app.models.admin import AdminUser
from app.services.admin.auth_service import AdminAuthService
from app.websocket.manager import websocket_manager
from app.utils.pagination import apply_pagination, get_total_count
from app.utils.response import format_list_response

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/orders", tags=["admin-orders"])


class OrderResponse(BaseModel):
    """Order response model."""

    id: int
    product_id: int
    product_name: Optional[str]
    full_name: str
    phone: str
    address: str
    city: Optional[str]
    quantity: int
    status: str
    created_at: str
    updated_at: Optional[str]

    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    """Order list response model."""

    orders: list[OrderResponse]
    total: int


class OrderStatusUpdate(BaseModel):
    """Order status update model."""

    status: str


@router.get("", response_model=OrderListResponse, status_code=status.HTTP_200_OK)
async def list_orders(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status"),
    date_from: Optional[str] = Query(None, description="Filter from date (ISO format)"),
    date_to: Optional[str] = Query(None, description="Filter to date (ISO format)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Page size"),
    current_admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> OrderListResponse:
    """
    List orders with filters - Refactored to use helpers.
    """
    # Build base query
    query = select(Order)

    # Apply filters
    filter_conditions = []
    if status_filter:
        filter_conditions.append(Order.status == status_filter)
    if date_from:
        try:
            date_from_obj = datetime.fromisoformat(date_from.replace("Z", "+00:00"))
            filter_conditions.append(Order.created_at >= date_from_obj)
        except ValueError:
            pass
    if date_to:
        try:
            date_to_obj = datetime.fromisoformat(date_to.replace("Z", "+00:00"))
            filter_conditions.append(Order.created_at <= date_to_obj)
        except ValueError:
            pass
    if filter_conditions:
        query = query.where(and_(*filter_conditions))

    # Get total count using helper
    total = await get_total_count(query, Order, db, filter_conditions)

    # Apply pagination using helper
    query = apply_pagination(query, page, page_size)
    query = query.order_by(Order.created_at.desc())

    # Execute query
    result = await db.execute(query)
    orders = result.scalars().all()

    # Build response
    order_list = [
        OrderResponse(
            id=o.id,
            product_id=o.product_id,
            product_name=o.product_name,
            full_name=o.full_name,
            phone=o.phone,
            address=o.address,
            city=o.city,
            quantity=o.quantity,
            status=o.status,
            created_at=o.created_at.isoformat() if o.created_at else "",
            updated_at=o.updated_at.isoformat() if o.updated_at else None,
        )
        for o in orders
    ]

    return OrderListResponse(orders=order_list, total=total)


@router.patch(
    "/{order_id}/status",
    response_model=OrderResponse,
    status_code=status.HTTP_200_OK,
)
async def update_order_status(
    order_id: int = Path(..., description="Order ID"),
    status_update: OrderStatusUpdate = ...,
    current_admin: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
) -> OrderResponse:
    """
    Update order status.
    """
    # Get order
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    # Update status
    old_status = order.status
    order.status = status_update.status
    order.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(order)

    # Log action
    await AdminAuthService.log_action(
        db,
        current_admin.id,
        "order_status_update",
        "success",
        resource_type="order",
        resource_id=order_id,
        details={"old_status": old_status, "new_status": status_update.status},
    )

    # Broadcast WebSocket event
    from app.websocket.events import create_event

    event = create_event(
        "order_status_changed",
        {
            "order_id": order_id,
            "old_status": old_status,
            "new_status": status_update.status,
        },
    )
    await websocket_manager.broadcast(event)

    return OrderResponse(
        id=order.id,
        product_id=order.product_id,
        product_name=order.product_name,
        full_name=order.full_name,
        phone=order.phone,
        address=order.address,
        city=order.city,
        quantity=order.quantity,
        status=order.status,
        created_at=order.created_at.isoformat() if order.created_at else "",
        updated_at=order.updated_at.isoformat() if order.updated_at else None,
    )
