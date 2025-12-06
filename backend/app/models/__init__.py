from app.database import Base

# Import all models so Alembic can detect them
from app.models.ads import ScrapedAd, ProductScore
from app.models.campaigns import Creative, Campaign
from app.models.orders import Order
from app.models.admin import AdminUser, AdminSession, AdminAction

__all__ = [
    "Base",
    "ScrapedAd",
    "ProductScore",
    "Creative",
    "Campaign",
    "Order",
    "AdminUser",
    "AdminSession",
    "AdminAction",
]
