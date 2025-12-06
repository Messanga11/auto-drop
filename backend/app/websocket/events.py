"""
WebSocket event types for admin real-time updates.

All events follow the pattern: {type: str, data: dict, timestamp: str}
"""

from datetime import datetime
from typing import Any, Dict, Literal, TypedDict

# Event types
EventType = Literal[
    # Dashboard events
    "dashboard_stats_updated",
    # Product events
    "product_scraped",
    "score_calculated",
    # Campaign events
    "campaign_status_changed",
    "campaign_activated",
    "campaign_deactivated",
    # Creative events
    "creative_generated",
    "creative_status_changed",
    # Order events
    "order_created",
    "order_status_changed",
    # Action events
    "scraping_progress",
    "scraping_completed",
    "scraping_failed",
    "scoring_progress",
    "scoring_completed",
    "scoring_failed",
    "creative_progress",
    "creative_completed",
    "creative_failed",
    # Connection events
    "connection_established",
    "connection_closed",
    "reconnect_requested",
]


class WebSocketEvent(TypedDict):
    """WebSocket event structure."""
    type: EventType
    data: Dict[str, Any]
    timestamp: str


def create_event(
    event_type: EventType,
    data: Dict[str, Any],
    timestamp: str | None = None,
) -> Dict[str, Any]:
    """
    Create a WebSocket event message.

    Args:
        event_type: Type of event
        data: Event payload
        timestamp: Optional timestamp (defaults to now)

    Returns:
        Event message dict
    """
    return {
        "type": event_type,
        "data": data,
        "timestamp": timestamp or datetime.utcnow().isoformat(),
    }


# Event payload schemas (for documentation)
# Dashboard stats updated
DashboardStatsUpdated = {
    "total_products": int,
    "scored_products": int,
    "top_5_products": list,
    "active_campaigns": int,
    "pending_orders": int,
}

# Product scraped
ProductScraped = {
    "product_id": int,
    "platform": str,
    "ad_id": str,
}

# Score calculated
ScoreCalculated = {
    "product_id": int,
    "score": float,
}

# Campaign status changed
CampaignStatusChanged = {
    "campaign_id": int,
    "old_status": str,
    "new_status": str,
}

# Order created
OrderCreated = {
    "order_id": int,
    "product_id": int,
    "status": str,
}

# Order status changed
OrderStatusChanged = {
    "order_id": int,
    "old_status": str,
    "new_status": str,
}

# Scraping progress
ScrapingProgress = {
    "progress": int,  # 0-100
    "ads_scraped": int,
    "status": str,
}

# Scoring progress
ScoringProgress = {
    "progress": int,  # 0-100
    "products_scored": int,
    "status": str,
}

# Creative progress
CreativeProgress = {
    "product_id": int,
    "progress": int,  # 0-100
    "status": str,
}

