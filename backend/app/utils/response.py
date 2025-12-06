"""
Response formatting utilities for API endpoints.
"""

from typing import Any, Dict, List


def format_list_response(
    items: List[Any],
    total: int,
    page: int,
    page_size: int
) -> Dict[str, Any]:
    """
    Format a list response with pagination metadata.
    
    Args:
        items: List of items to return
        total: Total number of items
        page: Current page number (1-indexed, must be >= 1)
        page_size: Number of items per page (must be >= 1)
    
    Returns:
        Dictionary with items, total, page, and page_size
    
    Raises:
        ValueError: If page < 1 or page_size < 1
    """
    if page < 1:
        raise ValueError("page must be >= 1")
    if page_size < 1:
        raise ValueError("page_size must be >= 1")
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
    }

