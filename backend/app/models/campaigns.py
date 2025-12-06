from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Creative(Base):
    __tablename__ = "creatives"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("scraped_ads.id"), nullable=False)
    video_id = Column(String(255))
    video_type = Column(String(50))
    status = Column(String(20))
    download_url = Column(Text)
    local_path = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime)

    # Relationships
    product = relationship("ScrapedAd", back_populates="creatives")


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("scraped_ads.id"), nullable=False)
    platform = Column(String(20), index=True)
    campaign_id = Column(String(255))
    campaign_name = Column(String(255))
    daily_budget = Column(Integer)
    status = Column(String(20), index=True)
    created_at = Column(DateTime, server_default=func.now())
    activated_at = Column(DateTime)
    meta_data = Column(JSONB)

    # Relationships
    product = relationship("ScrapedAd", back_populates="campaigns")

