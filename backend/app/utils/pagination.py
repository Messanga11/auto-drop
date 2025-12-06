"""
Pagination helper utilities for SQLAlchemy queries.
"""

from typing import Type
from sqlalchemy import Select, func
from sqlalchemy.ext.asyncio import AsyncSession


def apply_pagination(query: Select, page: int, page_size: int) -> Select:
    """
    Apply pagination to a SQLAlchemy query.
    
    Args:
        query: SQLAlchemy Select query
        page: Page number (1-indexed, must be >= 1)
        page_size: Number of items per page (must be >= 1)
    
    Returns:
        Query with offset and limit applied
    
    Raises:
        ValueError: If page < 1 or page_size < 1
    """
    if page < 1:
        raise ValueError("page must be >= 1")
    if page_size < 1:
        raise ValueError("page_size must be >= 1")
    
    offset = (page - 1) * page_size
    return query.offset(offset).limit(page_size)


async def get_total_count(
    query: Select,
    model: Type,
    db: AsyncSession,
    filters: list = None
) -> int:
    """
    Calculate total count of items for a query.
    
    Args:
        query: SQLAlchemy Select query (base query with filters)
        model: SQLAlchemy model class
        db: Async database session
        filters: Optional list of filter conditions to apply to count query
    
    Returns:
        Total number of items (int >= 0)
    """
    from sqlalchemy import select, func
    
    # Create count query from model
    count_query = select(func.count()).select_from(model)
    
    # Apply same filters if provided
    if filters:
        from sqlalchemy import and_
        count_query = count_query.where(and_(*filters))
    
    result = await db.execute(count_query)
    total = result.scalar() or 0
    return total

