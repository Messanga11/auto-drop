"""
Filtering helper utilities for SQLAlchemy queries.
"""

from typing import Any, Dict, Type
from sqlalchemy import Select, and_


def apply_filters(
    query: Select,
    model: Type,
    filters: Dict[str, Any]
) -> Select:
    """
    Apply filters dynamically to a SQLAlchemy query.
    
    Args:
        query: SQLAlchemy Select query
        model: SQLAlchemy model class
        filters: Dictionary of filters {field: value}
    
    Returns:
        Query with filters applied via .where()
    
    Note:
        - Ignores filters for non-existent columns
        - Supports None values (filters them out)
        - Supports empty string values (filters them out)
    """
    if not filters:
        return query
    
    filter_conditions = []
    
    for field, value in filters.items():
        # Skip None, empty strings, and non-existent columns
        if value is None or value == '':
            continue
        
        # Check if column exists in model
        if not hasattr(model, field):
            continue
        
        column = getattr(model, field)
        
        # Apply filter based on value type
        if isinstance(value, bool):
            filter_conditions.append(column == value)
        elif isinstance(value, (int, float)):
            filter_conditions.append(column == value)
        elif isinstance(value, str):
            # For string filters, support exact match
            filter_conditions.append(column == value)
        else:
            # For other types, use exact match
            filter_conditions.append(column == value)
    
    if filter_conditions:
        query = query.where(and_(*filter_conditions))
    
    return query

